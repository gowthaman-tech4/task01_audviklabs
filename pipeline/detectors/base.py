"""
Base classes and data structures for PII detection.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from abc import ABC, abstractmethod
from enum import Enum


class PIIType(Enum):
    """Enumeration of all PII types the pipeline can detect."""
    PERSON_NAME = "PERSON_NAME"
    SSN = "SSN"
    PAN = "PAN"
    AADHAAR = "AADHAAR"
    CREDIT_CARD = "CREDIT_CARD"
    PHONE = "PHONE"
    EMAIL = "EMAIL"
    DATE_OF_BIRTH = "DATE_OF_BIRTH"
    ADDRESS = "ADDRESS"
    ACCOUNT_NUMBER = "ACCOUNT_NUMBER"
    ORGANIZATION = "ORGANIZATION"
    IFSC_CODE = "IFSC_CODE"
    PASSPORT = "PASSPORT"
    VOTER_ID = "VOTER_ID"
    DRIVING_LICENSE = "DRIVING_LICENSE"
    COMPANY_ID = "COMPANY_ID"
    LOAN_NUMBER = "LOAN_NUMBER"
    POLICY_NUMBER = "POLICY_NUMBER"


@dataclass
class PIIEntity:
    """Represents a single detected PII entity in the text."""
    pii_type: PIIType
    value: str
    start: int          # Start character offset in source text
    end: int            # End character offset in source text
    confidence: float   # 0.0 to 1.0
    source: str         # "regex" or "ner" — which detector found it
    
    # V2 Enhancements
    source_scores: dict = field(default_factory=dict)
    calibrated_confidence: float = 0.0
    role: str = "UNKNOWN"
    relationship: str = ""
    section: str = "GENERIC"
    risk_score: float = 0.0
    decision: str = "PENDING"
    reason: str = ""

    def overlaps(self, other: 'PIIEntity') -> bool:
        """Check if this entity overlaps with another."""
        return self.start < other.end and other.start < self.end

    def contains(self, other: 'PIIEntity') -> bool:
        """Check if this entity fully contains another."""
        return self.start <= other.start and self.end >= other.end

    def overlap_ratio(self, other: 'PIIEntity') -> float:
        """Calculate the overlap ratio between two entities."""
        overlap_start = max(self.start, other.start)
        overlap_end = min(self.end, other.end)
        if overlap_start >= overlap_end:
            return 0.0
        overlap_len = overlap_end - overlap_start
        union_len = max(self.end, other.end) - min(self.start, other.start)
        return overlap_len / union_len if union_len > 0 else 0.0

    def __repr__(self):
        return (f"PIIEntity(type={self.pii_type.value}, "
                f"value='{self.value[:20]}...', "
                f"pos=[{self.start}:{self.end}], "
                f"conf={self.confidence:.2f}, "
                f"src={self.source})")


class PIIDetector(ABC):
    """Abstract base class for all PII detectors."""

    @abstractmethod
    def detect(self, text: str) -> List[PIIEntity]:
        """
        Detect PII entities in the given text.

        Args:
            text: The input text to scan for PII.

        Returns:
            A list of PIIEntity objects found in the text.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this detector."""
        pass
