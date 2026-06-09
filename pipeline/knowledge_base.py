"""
PII Knowledge Base — Policy-driven catalog defining risk levels, masking rules,
and regulatory context for each PII type across jurisdictions.
"""
from .detectors.base import PIIType
from .classifier import DocumentType


class PIIKnowledgeBase:
    """
    Enterprise Knowledge Base with jurisdiction-aware policies.

    Each policy group defines:
      - risk: float 0.0–1.0 (baseline risk for this entity type)
      - regulation: str (the regulatory framework requiring masking)
      - must_mask: bool (True = always mask regardless of risk score)
      - exceptions: list[str] (roles/contexts where masking can be skipped)
    """

    POLICIES = {
        "INDIAN_FINANCIAL": {
            PIIType.PAN: {
                "risk": 0.95,
                "regulation": "Income Tax Act, Section 139A",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.AADHAAR: {
                "risk": 0.95,
                "regulation": "Aadhaar Act 2016, Section 29",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.ACCOUNT_NUMBER: {
                "risk": 0.90,
                "regulation": "RBI Master Direction on KYC",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.IFSC_CODE: {
                "risk": 0.85,
                "regulation": "RBI — Bank routing code",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.CREDIT_CARD: {
                "risk": 0.95,
                "regulation": "PCI-DSS",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.PERSON_NAME: {
                "risk": 0.80,
                "regulation": "DPDP Act 2023",
                "must_mask": True,
                "exceptions": ["provider", "institution"]
            },
            PIIType.PHONE: {
                "risk": 0.65,
                "regulation": "DPDP Act 2023",
                "must_mask": False,
                "exceptions": ["provider", "institution"]
            },
            PIIType.EMAIL: {
                "risk": 0.70,
                "regulation": "DPDP Act 2023",
                "must_mask": False,
                "exceptions": ["provider", "institution"]
            },
            PIIType.ADDRESS: {
                "risk": 0.55,
                "regulation": "DPDP Act 2023",
                "must_mask": False,
                "exceptions": ["institution"]
            },
            PIIType.DATE_OF_BIRTH: {
                "risk": 0.80,
                "regulation": "DPDP Act 2023",
                "must_mask": False,
                "exceptions": []
            },
            PIIType.ORGANIZATION: {
                "risk": 0.20,
                "regulation": "N/A — Public entity",
                "must_mask": False,
                "exceptions": ["all"]
            },
            PIIType.LOAN_NUMBER: {
                "risk": 0.75,
                "regulation": "RBI Fair Practices Code",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.POLICY_NUMBER: {
                "risk": 0.75,
                "regulation": "IRDAI Guidelines",
                "must_mask": True,
                "exceptions": []
            },
        },

        "US_FINANCIAL": {
            PIIType.SSN: {
                "risk": 0.99,
                "regulation": "GLBA (Gramm-Leach-Bliley Act)",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.CREDIT_CARD: {
                "risk": 0.95,
                "regulation": "PCI-DSS",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.ACCOUNT_NUMBER: {
                "risk": 0.90,
                "regulation": "GLBA",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.PERSON_NAME: {
                "risk": 0.80,
                "regulation": "CCPA / GLBA",
                "must_mask": True,
                "exceptions": ["provider", "institution"]
            },
            PIIType.PHONE: {
                "risk": 0.65,
                "regulation": "TCPA / CCPA",
                "must_mask": False,
                "exceptions": ["provider", "institution"]
            },
            PIIType.EMAIL: {
                "risk": 0.70,
                "regulation": "CAN-SPAM / CCPA",
                "must_mask": False,
                "exceptions": ["provider", "institution"]
            },
            PIIType.ADDRESS: {
                "risk": 0.55,
                "regulation": "CCPA",
                "must_mask": False,
                "exceptions": ["institution"]
            },
            PIIType.DATE_OF_BIRTH: {
                "risk": 0.80,
                "regulation": "CCPA / HIPAA",
                "must_mask": False,
                "exceptions": []
            },
            PIIType.PASSPORT: {
                "risk": 0.95,
                "regulation": "Privacy Act 1974",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.DRIVING_LICENSE: {
                "risk": 0.85,
                "regulation": "DPPA (Driver's Privacy Protection Act)",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.ORGANIZATION: {
                "risk": 0.20,
                "regulation": "N/A — Public entity",
                "must_mask": False,
                "exceptions": ["all"]
            },
        },

        "MEDICAL": {
            PIIType.PERSON_NAME: {
                "risk": 0.90,
                "regulation": "HIPAA Safe Harbor — 18 identifiers",
                "must_mask": True,
                "exceptions": ["doctor", "physician", "provider"]
            },
            PIIType.DATE_OF_BIRTH: {
                "risk": 0.90,
                "regulation": "HIPAA Safe Harbor",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.PHONE: {
                "risk": 0.85,
                "regulation": "HIPAA Safe Harbor",
                "must_mask": True,
                "exceptions": ["provider"]
            },
            PIIType.EMAIL: {
                "risk": 0.85,
                "regulation": "HIPAA Safe Harbor",
                "must_mask": True,
                "exceptions": ["provider"]
            },
            PIIType.ADDRESS: {
                "risk": 0.80,
                "regulation": "HIPAA Safe Harbor",
                "must_mask": True,
                "exceptions": ["institution"]
            },
            PIIType.SSN: {
                "risk": 0.99,
                "regulation": "HIPAA Safe Harbor",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.ACCOUNT_NUMBER: {
                "risk": 0.90,
                "regulation": "HIPAA Safe Harbor",
                "must_mask": True,
                "exceptions": []
            },
            PIIType.ORGANIZATION: {
                "risk": 0.15,
                "regulation": "N/A — Hospital/Clinic names are public",
                "must_mask": False,
                "exceptions": ["all"]
            },
        },

        "GENERAL": {
            PIIType.PAN: {"risk": 0.95, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.AADHAAR: {"risk": 0.95, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.SSN: {"risk": 0.95, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.CREDIT_CARD: {"risk": 0.95, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.PASSPORT: {"risk": 0.95, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.ACCOUNT_NUMBER: {"risk": 0.90, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.VOTER_ID: {"risk": 0.90, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.DRIVING_LICENSE: {"risk": 0.85, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.COMPANY_ID: {"risk": 0.30, "regulation": "Generic PII Policy", "must_mask": False, "exceptions": []},
            PIIType.LOAN_NUMBER: {"risk": 0.75, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.POLICY_NUMBER: {"risk": 0.75, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": []},
            PIIType.EMAIL: {"risk": 0.70, "regulation": "Generic PII Policy", "must_mask": False, "exceptions": ["provider", "institution"]},
            PIIType.PHONE: {"risk": 0.65, "regulation": "Generic PII Policy", "must_mask": False, "exceptions": ["provider", "institution"]},
            PIIType.PERSON_NAME: {"risk": 0.80, "regulation": "Generic PII Policy", "must_mask": True, "exceptions": ["provider", "institution"]},
            PIIType.DATE_OF_BIRTH: {"risk": 0.80, "regulation": "Generic PII Policy", "must_mask": False, "exceptions": []},
            PIIType.ADDRESS: {"risk": 0.55, "regulation": "Generic PII Policy", "must_mask": False, "exceptions": ["institution"]},
            PIIType.ORGANIZATION: {"risk": 0.25, "regulation": "N/A — Public entity", "must_mask": False, "exceptions": ["all"]},
            PIIType.IFSC_CODE: {"risk": 0.85, "regulation": "N/A — Public routing code", "must_mask": True, "exceptions": []},
        },
    }

    # Map document types to their applicable jurisdiction
    DOC_TYPE_TO_JURISDICTION = {
        DocumentType.BANK_STATEMENT: "INDIAN_FINANCIAL",
        DocumentType.TAX_RETURN: "INDIAN_FINANCIAL",
        DocumentType.LOAN_DOCUMENT: "INDIAN_FINANCIAL",
        DocumentType.CREDIT_CARD_STATEMENT: "INDIAN_FINANCIAL",
        DocumentType.BROKERAGE_STATEMENT: "INDIAN_FINANCIAL",
        DocumentType.INSURANCE: "INDIAN_FINANCIAL",
        DocumentType.MEDICAL_RECORD: "MEDICAL",
        DocumentType.GENERIC: "GENERAL",
    }

    def _get_jurisdiction(self, doc_type: DocumentType) -> str:
        """Resolve the jurisdiction policy group for a document type."""
        return self.DOC_TYPE_TO_JURISDICTION.get(doc_type, "GENERAL")

    def get_policy(self, doc_type: DocumentType, pii_type: PIIType) -> dict:
        """
        Get the full policy entry for a PII type within a document's jurisdiction.
        Falls back to GENERAL if the jurisdiction doesn't define it.
        """
        jurisdiction = self._get_jurisdiction(doc_type)
        policies = self.POLICIES.get(jurisdiction, self.POLICIES["GENERAL"])
        policy = policies.get(pii_type)
        if policy is None:
            # Fallback to GENERAL
            policy = self.POLICIES["GENERAL"].get(pii_type)
        if policy is None:
            # Ultimate fallback
            return {"risk": 0.50, "regulation": "Unknown", "must_mask": False, "exceptions": []}
        return policy

    def get_base_risk(self, pii_type: PIIType, doc_type: DocumentType = None) -> float:
        """Get baseline risk for a PII type, optionally scoped to a document type."""
        if doc_type:
            return self.get_policy(doc_type, pii_type)["risk"]
        # Default: use GENERAL
        return self.get_policy(DocumentType.GENERIC, pii_type)["risk"]

    def is_must_mask(self, doc_type: DocumentType, pii_type: PIIType) -> bool:
        """Returns True if the regulation strictly demands masking."""
        return self.get_policy(doc_type, pii_type)["must_mask"]

    def get_regulation(self, doc_type: DocumentType, pii_type: PIIType) -> str:
        """Returns the regulation name that governs this entity in this document."""
        return self.get_policy(doc_type, pii_type)["regulation"]

    def get_exceptions(self, doc_type: DocumentType, pii_type: PIIType) -> list:
        """Returns the list of roles/contexts where masking can be skipped."""
        return self.get_policy(doc_type, pii_type)["exceptions"]

    def should_skip_for_role(self, doc_type: DocumentType, pii_type: PIIType, role: str) -> bool:
        """Check if a specific role is exempt from masking for this entity type."""
        exceptions = self.get_exceptions(doc_type, pii_type)
        if "all" in exceptions:
            return True
        return role.lower() in [e.lower() for e in exceptions]
