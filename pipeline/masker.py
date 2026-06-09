"""
PII Masker — replaces detected PII entities with typed placeholders
and generates a reversible mapping file.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from .detectors.base import PIIEntity, PIIType


class PIIMasker:
    """
    Masks PII entities in text with typed placeholders and produces
    a mapping file for recovery.
    """

    def __init__(self):
        self._counters: Dict[str, int] = {}

    def _get_placeholder(self, pii_type: PIIType) -> str:
        """Generate a unique placeholder for the given PII type."""
        type_name = pii_type.value
        self._counters[type_name] = self._counters.get(type_name, 0) + 1
        count = self._counters[type_name]
        return f"[{type_name}_{count:03d}]"

    def reset_counters(self):
        """Reset placeholder counters (call between documents)."""
        self._counters = {}

    def mask(self, text: str, entities: List[PIIEntity],
             document_name: str = "unknown") -> Tuple[str, Dict]:
        """
        Mask all PII entities in the text.

        Args:
            text: The original text.
            entities: List of detected PIIEntity objects.
            document_name: Name of the source document.

        Returns:
            Tuple of (masked_text, mapping_dict).
            mapping_dict contains all mappings for recovery.
        """
        if not entities:
            return text, self._build_mapping([], document_name)

        # Sort entities by start position (reverse) to replace from end → start
        # This preserves character offsets during replacement
        sorted_entities = sorted(entities, key=lambda e: e.start, reverse=True)

        # Remove any duplicate/overlapping entities (keep first occurrence)
        filtered_entities = self._remove_duplicates(sorted_entities)

        masked_text = text
        mappings = []

        for entity in filtered_entities:
            placeholder = self._get_placeholder(entity.pii_type)

            # Replace in text
            masked_text = (
                masked_text[:entity.start] +
                placeholder +
                masked_text[entity.end:]
            )

            mappings.append({
                "placeholder": placeholder,
                "original": entity.value,
                "type": entity.pii_type.value,
                "confidence": round(entity.confidence, 3),
                "source": entity.source,
                "position": {
                    "start": entity.start,
                    "end": entity.end
                }
            })

        # Reverse mappings so they're in document order (start → end)
        mappings.reverse()

        mapping_dict = self._build_mapping(mappings, document_name)
        return masked_text, mapping_dict

    def _remove_duplicates(self, sorted_entities: List[PIIEntity]) -> List[PIIEntity]:
        """Remove overlapping entities from a reverse-sorted list."""
        if not sorted_entities:
            return []

        filtered = [sorted_entities[0]]
        for entity in sorted_entities[1:]:
            # Check if this entity overlaps with any already accepted entity
            if not any(entity.overlaps(accepted) for accepted in filtered):
                filtered.append(entity)

        return filtered

    def _build_mapping(self, mappings: List[Dict],
                       document_name: str) -> Dict:
        """Build the complete mapping dictionary."""
        return {
            "document": document_name,
            "timestamp": datetime.now().isoformat(),
            "total_entities_masked": len(mappings),
            "entity_type_counts": self._count_by_type(mappings),
            "mappings": mappings
        }

    def _count_by_type(self, mappings: List[Dict]) -> Dict[str, int]:
        """Count entities by type."""
        counts: Dict[str, int] = {}
        for m in mappings:
            t = m["type"]
            counts[t] = counts.get(t, 0) + 1
        return counts

    @staticmethod
    def unmask(masked_text: str, mapping_dict: Dict) -> str:
        """
        Recover the original text from masked text and mapping.

        Args:
            masked_text: The masked text with placeholders.
            mapping_dict: The mapping dictionary produced by mask().

        Returns:
            The original text with PII restored.
        """
        result = masked_text
        # Replace in reverse order of placeholder to handle nested cases
        for mapping in reversed(mapping_dict.get("mappings", [])):
            placeholder = mapping["placeholder"]
            original = mapping["original"]
            result = result.replace(placeholder, original, 1)
        return result

    @staticmethod
    def save_mapping(mapping_dict: Dict, output_path: str):
        """Save mapping to a JSON file."""
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapping_dict, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_mapping(mapping_path: str) -> Dict:
        """Load mapping from a JSON file."""
        with open(mapping_path, 'r', encoding='utf-8') as f:
            return json.load(f)
