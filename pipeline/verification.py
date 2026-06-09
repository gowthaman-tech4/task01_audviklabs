from typing import List, Tuple
from .detectors.base import PIIEntity, PIIType

class MultiPassVerifier:
    """
    Runs a second pass on masked text to catch residual PII leaks.
    """

    def __init__(self, pipeline_ref):
        # We take a reference to the pipeline to run the second pass
        self.pipeline = pipeline_ref

    def verify(self, masked_text: str, original_entities: List[PIIEntity] = None) -> Tuple[bool, List[PIIEntity]]:
        """
        Returns (passed_verification, residual_entities).
        """
        # Run detection ONLY (steps 1-4 of pipeline)
        # We don't want to run the full pipeline recursively to avoid infinite loops.
        # But for simplicity, we can use the pipeline's detector methods directly.
        
        # Step 1: Context
        entities = self.pipeline._context_detector.detect(masked_text)
        
        # Step 2: Presidio
        if self.pipeline._use_presidio and self.pipeline._presidio_detector:
            entities.extend(self.pipeline._presidio_detector.detect(masked_text))

        # We skip layoutLM for verification pass as it requires coordinates which we don't map back

        # Filter out the placeholders themselves (e.g. [PERSON_NAME_001])
        residual_entities = []
        for ent in entities:
            import re
            val = ent.value.strip()
            # If the value is a placeholder or part of a placeholder, ignore it
            if val.startswith('[') and val.endswith(']') and '_' in val:
                continue
            if re.search(r"\b[A-Z_]+_\d{3}\b", val) or "[" in val or "]" in val or "█" in val:
                continue
                
            # If it's a real entity that survived masking, flag it
            residual_entities.append(ent)

        # Step 3: Check for partial leaks of original high-sensitivity entities
        if original_entities:
            for ent in original_entities:
                if ent.pii_type in [PIIType.PAN, PIIType.AADHAAR, PIIType.SSN, PIIType.CREDIT_CARD, PIIType.ACCOUNT_NUMBER, PIIType.EMAIL, PIIType.PHONE]:
                    val = ent.value.strip()
                    if len(val) >= 5:
                        # Check all 5-character substrings of the original value
                        for i in range(len(val) - 4):
                            sub = val[i:i+5]
                            # Skip if substring contains placeholder-like chars
                            if any(c in sub for c in ['[', ']', '_', '*', '█']):
                                continue
                            if sub in masked_text:
                                leak_idx = masked_text.find(sub)
                                # Avoid duplicate residual entities for overlapping ranges
                                if not any(r.start <= leak_idx < r.end for r in residual_entities):
                                    residual_entities.append(PIIEntity(
                                        pii_type=ent.pii_type,
                                        value=sub,
                                        start=leak_idx,
                                        end=leak_idx + len(sub),
                                        confidence=1.0,
                                        source="leak_verification"
                                    ))
                                    break
            
        return len(residual_entities) == 0, residual_entities
