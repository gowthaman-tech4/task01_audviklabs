import re
from typing import List
from .detectors.base import PIIEntity, PIIType

class RelationshipExtractor:
    """
    Assigns roles and relationships to entities based on preceding context labels.
    """

    ROLE_PATTERNS = {
        "SUBJECT": [
            r"(?i)\b(?:customer|borrower|applicant|patient|insured|holder|employee|student)\b"
        ],
        "PROVIDER": [
            r"(?i)\b(?:doctor|physician|dr\.|attorney|judge|employer|manager)\b"
        ],
        "RELATED_PARTY": [
            r"(?i)\b(?:witness|nominee|co-borrower|spouse|guardian|beneficiary)\b"
        ],
        "INSTITUTION": [
            r"(?i)\b(?:company|bank|lender|insurer|deductor|college|university|hospital|clinic)\b"
        ]
    }

    def extract(self, entities: List[PIIEntity], text: str) -> List[PIIEntity]:
        for ent in entities:
            # We mostly care about roles for names and organizations
            if ent.pii_type not in (PIIType.PERSON_NAME, PIIType.ORGANIZATION):
                ent.role = "UNKNOWN"
                continue

            window_start = max(0, ent.start - 60)
            context = text[window_start:ent.start]

            assigned_role = "UNKNOWN"
            # Check context backwards (closest labels have higher priority)
            for role, patterns in self.ROLE_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, context):
                        assigned_role = role
                        break
                if assigned_role != "UNKNOWN":
                    break
            
            ent.role = assigned_role

            # Infer relationship based on role
            if assigned_role == "SUBJECT":
                ent.relationship = "Primary Subject"
            elif assigned_role == "PROVIDER":
                ent.relationship = "Service Provider / Authority"
            elif assigned_role == "RELATED_PARTY":
                ent.relationship = "Secondary Party"
            elif assigned_role == "INSTITUTION":
                ent.relationship = "Corporate Entity"
            else:
                ent.relationship = "Unspecified"

        return entities
