from typing import List
from .detectors.base import PIIEntity

class ConfidenceCalibrator:
    """
    Computes a calibrated ensemble confidence score based on the source detectors
    that identified the entity.
    """
    
    # Base weight for each detector type
    SOURCE_WEIGHTS = {
        "regex": 0.95,      # Presidio regex pattern matching
        "context": 0.90,    # Context detector (label-value)
        "presidio": 0.70,   # Presidio NER model
        "layoutlm": 0.75,   # Layout-aware detection
        "propagation": 0.85 # Propagated seeds
    }

    def calibrate(self, entities: List[PIIEntity]) -> List[PIIEntity]:
        for ent in entities:
            if not ent.source_scores:
                # Fallback if merger didn't track sources (shouldn't happen)
                ent.calibrated_confidence = ent.confidence
                continue

            # Calculate weighted average
            total_weight = 0.0
            weighted_sum = 0.0
            
            for source, conf in ent.source_scores.items():
                # Map source name to generic weights if specific not found
                base_source = source.lower()
                weight = self.SOURCE_WEIGHTS.get(base_source, 0.5)
                
                # Presidio might return "presidio" for both regex and NER,
                # but if confidence is very high (>0.85), we treat it as regex
                if base_source == "presidio" and conf >= 0.85:
                    weight = self.SOURCE_WEIGHTS["regex"]

                weighted_sum += conf * weight
                total_weight += weight

            calibrated = weighted_sum / total_weight if total_weight > 0 else ent.confidence

            # Bonus / Penalty based on ensemble agreement
            num_sources = len(ent.source_scores)
            if num_sources == 1:
                # Single source penalty
                calibrated *= 0.90
            elif num_sources >= 3:
                # Multiple source agreement bonus
                calibrated *= 1.15

            # Clamp between 0 and 1
            ent.calibrated_confidence = max(0.0, min(1.0, calibrated))

        return entities
