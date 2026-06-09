"""
Entity merger — combines results from multiple detectors,
resolves overlaps, deduplicates, and produces a unified entity list.
"""
from typing import List
from .detectors.base import PIIEntity, PIIType


class EntityMerger:
    """
    Merges PII entities from multiple detection sources.

    Resolution strategy:
    1. If two entities overlap and have the same type → keep higher confidence.
    2. If two entities overlap with different types → keep the more specific
       (regex > ner for structured types like SSN/PAN; ner > regex for names).
    3. If one entity fully contains another → keep the larger one.
    4. Non-overlapping entities are all kept.
    """

    # Types where regex is generally more reliable than NER
    REGEX_PREFERRED_TYPES = {
        PIIType.SSN, PIIType.PAN, PIIType.AADHAAR,
        PIIType.CREDIT_CARD, PIIType.PHONE, PIIType.EMAIL,
        PIIType.ACCOUNT_NUMBER, PIIType.IFSC_CODE,
        PIIType.PASSPORT, PIIType.VOTER_ID, PIIType.DRIVING_LICENSE,
        PIIType.COMPANY_ID
    }

    # Types where NER is generally more reliable
    NER_PREFERRED_TYPES = {
        PIIType.PERSON_NAME, PIIType.ORGANIZATION, PIIType.ADDRESS
    }

    def __init__(self, overlap_threshold: float = 0.3):
        """
        Args:
            overlap_threshold: Minimum overlap ratio to consider two entities
                              as overlapping (0.0 to 1.0).
        """
        self.overlap_threshold = overlap_threshold

    def merge(self, *entity_lists: List[PIIEntity]) -> List[PIIEntity]:
        """
        Merge multiple lists of PIIEntity objects into a single deduplicated list.
        """
        # Flatten all entities into one list and init source_scores
        all_entities = []
        for entity_list in entity_lists:
            for ent in entity_list:
                if not ent.source_scores:
                    ent.source_scores = {ent.source: ent.confidence}
                all_entities.append(ent)

        if not all_entities:
            return []

        # Sort by start position, then by length (longer first)
        all_entities.sort(key=lambda e: (e.start, -(e.end - e.start)))

        # Resolve overlaps
        resolved = []
        for entity in all_entities:
            merged = False
            for i, existing in enumerate(resolved):
                if entity.overlaps(existing):
                    # Decide which one to keep, but combine source_scores
                    winner = self._resolve_overlap(existing, entity)
                    
                    # Combine source scores into the winner
                    combined_scores = existing.source_scores.copy()
                    for src, conf in entity.source_scores.items():
                        if src not in combined_scores or conf > combined_scores[src]:
                            combined_scores[src] = conf
                    winner.source_scores = combined_scores
                    
                    resolved[i] = winner
                    merged = True
                    break

            if not merged:
                resolved.append(entity)

        # Final sort by position
        resolved.sort(key=lambda e: e.start)

        return resolved

    def _get_priority(self, entity: PIIEntity) -> float:
        """
        Assigns a priority score (0.0 to 100.0) to resolve overlaps.
        Regex/context matching on structured PII has the highest priority.
        """
        is_regex = (entity.source == "context" or 
                    (entity.source == "presidio" and entity.pii_type in self.REGEX_PREFERRED_TYPES))
        
        if is_regex:
            if entity.pii_type in [PIIType.PAN, PIIType.AADHAAR, PIIType.SSN, PIIType.PHONE, PIIType.EMAIL]:
                return 100.0
            if entity.pii_type in self.REGEX_PREFERRED_TYPES:
                return 95.0
                
        if entity.source == "layoutlm":
            return 80.0
            
        if entity.source in ["presidio", "ner"]:
            return 60.0
            
        return 50.0

    def _resolve_overlap(self, entity_a: PIIEntity,
                         entity_b: PIIEntity) -> PIIEntity:
        """
        Resolve overlap between two entities. Returns the winner.
        """
        # Case 1: Same type — keep higher confidence
        if entity_a.pii_type == entity_b.pii_type:
            return entity_a if entity_a.confidence >= entity_b.confidence else entity_b

        # Case 2: One contains another.
        # If the smaller one is a critical must-mask regex (priority 100, like PAN/Aadhaar/SSN), it wins!
        pri_a = self._get_priority(entity_a)
        pri_b = self._get_priority(entity_b)

        if entity_a.contains(entity_b) and pri_b == 100.0:
            return entity_b
        if entity_b.contains(entity_a) and pri_a == 100.0:
            return entity_a

        # Otherwise, keep the larger enclosing entity
        if entity_a.contains(entity_b):
            return entity_a
        if entity_b.contains(entity_a):
            return entity_b

        # Case 3: Priority-based resolution for partial overlaps
        if abs(pri_a - pri_b) > 1.0:
            return entity_a if pri_a > pri_b else entity_b

        # Fallback: prefer higher confidence
        return entity_a if entity_a.confidence >= entity_b.confidence else entity_b
