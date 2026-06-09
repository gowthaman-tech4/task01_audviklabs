"""
Risk Scoring Engine — Computes a 0.0-1.0 risk score for entities
and assigns a decision routing based on context, role, section, and policy.
"""
from typing import List
from .detectors.base import PIIEntity, PIIType
from .classifier import DocumentType
from .knowledge_base import PIIKnowledgeBase


class RiskScoringEngine:
    """
    Computes a 0.0-1.0 risk score for entities and assigns a decision routing.
    Integrates the jurisdiction-aware Knowledge Base for policy lookups.
    """

    def __init__(self):
        self.kb = PIIKnowledgeBase()

        # Thresholds
        self.THRESHOLD_AUTO_MASK = 0.70
        self.THRESHOLD_REVIEW = 0.40  # Between 0.40 and 0.70 is REVIEW (or LLM)

    def calculate_risk(self, entities: List[PIIEntity], doc_type: DocumentType, text: str = None) -> List[PIIEntity]:
        for ent in entities:
            # 0. Context-Aware Overrides (Bank Name & Employer Rules)
            val_lower = ent.value.lower()
            
            # Bank Name Rule: Only for ORGANIZATION
            if ent.pii_type == PIIType.ORGANIZATION and "bank" in val_lower:
                ent.risk_score = 0.10
                ent.decision = "AUTO_KEEP"
                ent.reason = "Financial KB: Bank name is kept."
                continue

            # Employer Name Rule:
            if text:
                window_left = text[max(0, ent.start - 80):ent.start].lower()
                is_employer_context = any(kw in window_left for kw in ["employer", "deductor", "deduct", "organization of employment"])
                
                if is_employer_context:
                    if ent.pii_type == PIIType.ORGANIZATION:
                        ent.risk_score = 0.15
                        ent.decision = "AUTO_KEEP"
                        ent.reason = "Financial KB: Employer organization name is kept."
                        continue
                    elif ent.pii_type == PIIType.PERSON_NAME:
                        ent.risk_score = 0.50
                        ent.decision = "REVIEW"
                        ent.reason = "Financial KB: Person name associated with employer context requires review."
                        continue

            # 1. Get full policy from Knowledge Base (jurisdiction-aware)
            policy = self.kb.get_policy(doc_type, ent.pii_type)
            base_risk = policy["risk"]
            
            # Custom Address Risk Scoring
            if ent.pii_type == PIIType.ADDRESS:
                base_risk = self._calculate_address_risk(ent.value)

            regulation = policy["regulation"]
            risk = base_risk

            # 2. Must-Mask Override (regulatory hard requirement)
            if policy["must_mask"]:
                # Check if the entity's role is an exception
                role = getattr(ent, 'role', 'UNKNOWN')
                if self.kb.should_skip_for_role(doc_type, ent.pii_type, role):
                    # Role is exempt — don't force mask, but keep risk elevated
                    risk *= 0.5
                else:
                    ent.risk_score = 1.0
                    ent.decision = "AUTO_MASK"
                    ent.reason = f"Regulatory: {regulation} requires masking {ent.pii_type.value} in {doc_type.value}"
                    continue

            # 3. Apply Section Multipliers
            section = getattr(ent, 'section', 'GENERIC')
            if section in ["PERSONAL_INFO", "MEDICAL_HISTORY", "BANK_DETAILS"]:
                risk *= 1.3
            elif section in ["EMPLOYMENT"]:
                risk *= 1.0  # Neutral
            elif section in ["TRANSACTION_HISTORY", "LEGAL_TERMS"]:
                risk *= 0.8

            # 4. Apply Role Multipliers (for names/orgs)
            role = getattr(ent, 'role', 'UNKNOWN')
            if role == "SUBJECT":
                risk *= 1.3
            elif role == "RELATED_PARTY":
                risk *= 1.1
            elif role == "PROVIDER":
                risk *= 0.4
            elif role == "INSTITUTION":
                risk *= 0.3

            # 5. Apply Confidence Weight
            conf = getattr(ent, 'calibrated_confidence', ent.confidence)
            # Center around 0.8: conf=0.9 boosts, conf=0.5 drops
            risk *= (conf / 0.8)

            # Clamp risk
            risk = max(0.0, min(1.0, risk))
            ent.risk_score = round(risk, 4)

            # 6. Assign Decision
            if risk >= self.THRESHOLD_AUTO_MASK:
                ent.decision = "AUTO_MASK"
                ent.reason = f"High risk ({risk:.2f}) — {regulation}"
            elif risk >= self.THRESHOLD_REVIEW:
                ent.decision = "REVIEW"
                ent.reason = f"Medium risk ({risk:.2f}) — requires verification — {regulation}"
            else:
                ent.decision = "AUTO_KEEP"
                ent.reason = f"Low risk ({risk:.2f}) — safe context — {regulation}"

        return entities

    def _calculate_address_risk(self, value: str) -> float:
        import re
        val_lower = value.lower()
        cleaned = val_lower.strip(",. \t\n\r")
        
        # 1. Indian PIN code (exactly 6 digits)
        if re.match(r"^\d{6}$", cleaned):
            return 0.85

        # 2. Check if State alone
        indian_states = [
            "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat", 
            "haryana", "himachal pradesh", "jharkhand", "karnataka", "kerala", "madhya pradesh", 
            "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab", 
            "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura", "uttar pradesh", 
            "uttarakhand", "west bengal", "delhi", "jammu & kashmir", "jammu and kashmir", "ladakh",
            "puducherry", "chandigarh", "dadra and nagar haveli", "daman and diu", "lakshadweep", "andaman and nicobar"
        ]
        us_states = [
            "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware",
            "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky",
            "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
            "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico",
            "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania",
            "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont",
            "virginia", "washington", "west virginia", "wisconsin", "wyoming"
        ]
        
        if cleaned in indian_states or cleaned in us_states:
            return 0.20
            
        # 3. Check if City alone (no street words and no digits, <= 2 words)
        street_keywords = [
            "street", "st.", "st", "road", "rd.", "rd", "lane", "ln", "avenue", "ave", "cross", "main",
            "nagar", "colony", "extension", "ext", "floor", "flat", "apartment", "apt", "building", "bldg",
            "plot", "door", "house", "h.no", "sector", "phase", "block", "#", "ward"
        ]
        
        has_street = any(re.search(rf"\b{kw}\b", val_lower) for kw in street_keywords) or "#" in val_lower
        has_digits = any(c.isdigit() for c in val_lower)
        
        word_count = len(cleaned.split())
        if not has_street and not has_digits and word_count <= 2:
            return 0.25
            
        # 4. Full address containing street details or numbers
        if has_street or has_digits:
            return 0.90
            
        return 0.55
