"""
Main PII Masking Pipeline — orchestrates ingestion, detection, merging, and masking.
"""
import os
import json
import glob
import re
from typing import List, Dict, Tuple, Optional
from .ingestion import DocumentIngester, CoordinateAwareResult
from .detectors.base import PIIEntity, PIIType
from .merger import EntityMerger
from .masker import PIIMasker
from .detectors.context_detector import ContextDetector
from .classifier import DocumentClassifier, DocumentType

# V2 Enhancements
from .section_detector import SectionDetector
from .confidence_calibrator import ConfidenceCalibrator
from .relationship_extractor import RelationshipExtractor
from .risk_scoring import RiskScoringEngine
from .llm_verifier import LLMVerifier
from .verification import MultiPassVerifier


class PIIPipeline:
    """
    End-to-end PII masking pipeline (V2 Enterprise Edition).
    """

    def __init__(self, spacy_model: str = "en_core_web_sm",
                 use_ner: bool = True,
                 confidence_threshold: float = 0.5):
        """Initialize the 12-stage V2 pipeline."""
        # Stage 1
        self._ingester = DocumentIngester()
        # Stage 2
        self._classifier = DocumentClassifier()
        # Stage 3
        self._section_detector = SectionDetector()
        
        # Stage 4
        self._context_detector = ContextDetector()
        self._presidio_detector = None
        self._use_presidio = True
        try:
            from .detectors.presidio_detector import PresidioDetector
            self._presidio_detector = PresidioDetector(model_name="en_core_web_sm")
        except (ImportError, OSError) as e:
            print(f"[WARN] Presidio detector unavailable: {e}")
            self._use_presidio = False

        self._layoutlm_detector = None
        self._use_layoutlm = True
        try:
            from .detectors.layoutlm_detector import LayoutLMDetector
            self._layoutlm_detector = LayoutLMDetector()
        except Exception as e:
            print(f"[WARN] LayoutLM detector unavailable: {e}")
            self._use_layoutlm = False

        # Stage 5
        self._merger = EntityMerger()
        self._confidence_calibrator = ConfidenceCalibrator()
        
        # Stage 6
        self._relationship_extractor = RelationshipExtractor()
        
        # Stage 7 & 8
        self._risk_scorer = RiskScoringEngine()
        
        # Stage 9
        self._llm_verifier = LLMVerifier(model_name="llama3.2")
        
        # Stage 11 (Stage 10 is UI Review - bypassed here)
        self._masker = PIIMasker()
        self._verifier = MultiPassVerifier(self)
        
        self._confidence_threshold = confidence_threshold
        self.last_audit_trail = []

    def process_text(self, text: str,
                     document_name: str = "unknown",
                     coord_result: Optional[CoordinateAwareResult] = None) -> Tuple[str, Dict, List[PIIEntity]]:
        """
        Process raw text through the 12-stage V2 pipeline.
        """
        self._masker.reset_counters()

        # Step 2: Classify document
        doc_type = self._classifier.classify(text)

        # Step 3: Section Detection
        sections = self._section_detector.detect(text)

        # Step 4: Hybrid Candidate Generation
        merged_entities = self._context_detector.detect(text)

        if self._use_presidio and self._presidio_detector:
            presidio_entities = self._presidio_detector.detect(text)
            merged_entities.extend(presidio_entities)

        # Decide whether to run LayoutLM on high-risk sections
        if self._use_layoutlm and self._layoutlm_detector and coord_result is not None:
            high_risk_sections = [s for s in sections if s.risk_level == "HIGH"]
            
            run_layoutlm = False
            sections_to_run = []
            
            for sec in high_risk_sections:
                has_high_conf = False
                for ent in merged_entities:
                    if sec.start <= ent.start <= sec.end and ent.confidence >= 0.9:
                        has_high_conf = True
                        break
                if not has_high_conf:
                    run_layoutlm = True
                    sections_to_run.append(sec)
            
            if run_layoutlm:
                # Create a filtered coord_result containing only word_boxes in high-risk sections to run
                from copy import copy
                filtered_coord = copy(coord_result)
                high_risk_boxes = set()
                
                for sec in sections_to_run:
                    for ci in range(sec.start, min(sec.end, len(text))):
                        if ci in coord_result.char_to_boxes:
                            for box in coord_result.char_to_boxes[ci]:
                                high_risk_boxes.add(id(box))
                                
                filtered_coord.word_boxes = [wb for wb in coord_result.word_boxes if id(wb) in high_risk_boxes]
                
                if filtered_coord.word_boxes:
                    layoutlm_entities = self._layoutlm_detector.detect(text, coord_result=filtered_coord)
                    merged_entities.extend(layoutlm_entities)

        # Reclassify type conflicts
        for e in merged_entities:
            if e.pii_type == PIIType.PERSON_NAME:
                val_lower = e.value.lower()
                org_keywords = [
                    "corp", "corporation", "inc", "ltd", "limited", "co", "company",
                    "finance", "securities", "insurance", "bank", "union", "association",
                    "credit", "capital", "housing", "shield", "trust", "lending", "funding"
                ]
                words = re.findall(r"\b\w+\b", val_lower)
                if any(kw in words for kw in org_keywords):
                    e.pii_type = PIIType.ORGANIZATION

        # Filter out invalid multiline entities (only ADDRESS can have newlines)
        valid_entities = []
        for e in merged_entities:
            if e.pii_type != PIIType.ADDRESS and ('\n' in e.value or '\r' in e.value):
                continue
            valid_entities.append(e)

        # Step 5: Merge overlaps and Calibrate Confidence
        merged_entities = self._merger.merge(valid_entities)
        merged_entities = self._confidence_calibrator.calibrate(merged_entities)

        # Map entities to sections
        for ent in merged_entities:
            ent.section = "GENERIC"
            for sec in sections:
                if sec.start <= ent.start <= sec.end:
                    ent.section = sec.name
                    break

        # Step 6: Relationship Extraction
        merged_entities = self._relationship_extractor.extract(merged_entities, text)

        # Step 7 & 8: Risk Scoring Engine (includes KB lookup internally)
        merged_entities = self._risk_scorer.calculate_risk(merged_entities, doc_type, text)

        # Step 9: LLM Verification for 'REVIEW' tier entities
        merged_entities = self._llm_verifier.verify(merged_entities, text, doc_type)

        # Generate Audit Log & Filter Entities to Mask
        filtered_entities = []
        audit_trail = []

        for ent in merged_entities:
            # For V2, we only mask if decision is AUTO_MASK
            # If REVIEW is bypassed or LLM failed, they default to AUTO_MASK
            should_mask = (ent.decision == "AUTO_MASK")

            audit_trail.append({
                "type": ent.pii_type.name,
                "value": ent.value,
                "start": ent.start,
                "end": ent.end,
                "confidence": round(getattr(ent, 'calibrated_confidence', ent.confidence), 3),
                "source": ent.source,
                "section": getattr(ent, 'section', 'GENERIC'),
                "role": getattr(ent, 'role', 'UNKNOWN'),
                "risk_score": getattr(ent, 'risk_score', 0.0),
                "decision": ent.decision,
                "matching_reason": getattr(ent, 'reason', '')
            })
            if should_mask:
                filtered_entities.append(ent)
                
        self.last_audit_trail = audit_trail

        # Step 11: Mask the text
        masked_text, mapping = self._masker.mask(
            text, filtered_entities, document_name
        )

        # Multi-Pass Verification
        passed, residuals = self._verifier.verify(masked_text, filtered_entities)
        if not passed:
            print(f"[WARN] Multi-pass caught {len(residuals)} residual leaks! Appending to audit log.")
            for r in residuals:
                audit_trail.append({
                    "type": r.pii_type.name,
                    "value": r.value,
                    "start": r.start,
                    "end": r.end,
                    "confidence": round(r.confidence, 3),
                    "source": "Verification Pass",
                    "section": "UNKNOWN",
                    "role": "UNKNOWN",
                    "risk_score": 1.0,
                    "decision": "AUTO_MASK (Pass 2)",
                    "matching_reason": "Caught during residual leak verification pass"
                })
            # Re-mask with residuals
            masked_text, mapping2 = self._masker.mask(masked_text, residuals, document_name + "_pass2")
            mapping["mappings"].extend(mapping2["mappings"])
            filtered_entities.extend(residuals)

        return masked_text, mapping, filtered_entities

    def process_file(self, file_path: str,
                     force_ocr: bool = False) -> Tuple[str, Dict, List[PIIEntity], CoordinateAwareResult]:
        """
        Process a single file through the pipeline using coordinate-aware extraction.
        """
        coord_result = self._ingester.extract_with_coordinates(file_path)
        doc_name = os.path.basename(file_path)

        masked_text, mapping, entities = self.process_text(
            coord_result.full_text, 
            document_name=doc_name, 
            coord_result=coord_result
        )
        return masked_text, mapping, entities, coord_result

    def process_directory(self, input_dir: str, output_dir: str,
                          mapping_dir: str,
                          extensions: Optional[List[str]] = None) -> Dict:
        """
        Process all documents in a directory.
        """
        if extensions is None:
            extensions = ['.txt', '.pdf', '.png', '.jpg']

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(mapping_dir, exist_ok=True)

        results = {
            "total_files": 0,
            "processed": 0,
            "failed": 0,
            "total_entities": 0,
            "files": []
        }

        files = []
        for ext in extensions:
            files.extend(glob.glob(os.path.join(input_dir, f"*{ext}")))

        results["total_files"] = len(files)

        for file_path in sorted(files):
            file_name = os.path.basename(file_path)
            base_name = os.path.splitext(file_name)[0]

            try:
                masked_text, mapping, entities, coord_result = self.process_file(file_path)

                output_path = os.path.join(output_dir, f"{base_name}_masked.txt")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(masked_text)

                mapping_path = os.path.join(mapping_dir, f"{base_name}_mapping.json")
                PIIMasker.save_mapping(mapping, mapping_path)

                results["processed"] += 1
                results["total_entities"] += len(entities)
                results["files"].append({
                    "file": file_name,
                    "status": "success",
                    "entities_found": len(entities),
                    "entity_types": mapping.get("entity_type_counts", {})
                })

                print(f"  [OK] {file_name}: {len(entities)} entities masked")

            except Exception as e:
                results["failed"] += 1
                results["files"].append({
                    "file": file_name,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"  [FAIL] {file_name}: {str(e)}")

        return results

