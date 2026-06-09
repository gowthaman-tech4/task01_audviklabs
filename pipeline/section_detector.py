import re
from typing import List
from dataclasses import dataclass

@dataclass
class DocumentSection:
    name: str
    risk_level: str  # "HIGH", "MEDIUM", "LOW"
    start: int
    end: int

class SectionDetector:
    """
    Detects logical sections in a document and assigns risk levels.
    """
    
    SECTION_PATTERNS = {
        "PERSONAL_INFO": {
            "keywords": [r"(?i)\bpersonal information\b", r"(?i)\bpatient details\b", r"(?i)\bcustomer details\b", r"(?i)\bprofile\b"],
            "risk_level": "HIGH"
        },
        "EMPLOYMENT": {
            "keywords": [r"(?i)\bemployment details\b", r"(?i)\bemployer information\b", r"(?i)\bschedule of salary\b"],
            "risk_level": "MEDIUM"
        },
        "TAX_DETAILS": {
            "keywords": [r"(?i)\btax details\b", r"(?i)\btax summary\b", r"(?i)\bincome tax\b"],
            "risk_level": "MEDIUM"
        },
        "TRANSACTION_HISTORY": {
            "keywords": [r"(?i)\btransaction history\b", r"(?i)\baccount activity\b", r"(?i)\bstatement of transactions\b"],
            "risk_level": "LOW"
        },
        "LEGAL_TERMS": {
            "keywords": [r"(?i)\bterms and conditions\b", r"(?i)\bdeclaration\b", r"(?i)\bagreement terms\b"],
            "risk_level": "LOW"
        },
        "BANK_DETAILS": {
            "keywords": [r"(?i)\bbank details\b", r"(?i)\baccount details\b", r"(?i)\bpayment information\b"],
            "risk_level": "HIGH"
        },
        "MEDICAL_HISTORY": {
            "keywords": [r"(?i)\bmedical history\b", r"(?i)\bdiagnosis\b", r"(?i)\btreatment plan\b", r"(?i)\bclinical notes\b"],
            "risk_level": "HIGH"
        }
    }

    def detect(self, text: str) -> List[DocumentSection]:
        sections = []
        found_headers = []

        # Find all section headers
        for sec_name, sec_data in self.SECTION_PATTERNS.items():
            for pattern in sec_data["keywords"]:
                for match in re.finditer(pattern, text):
                    # Ensure it's acting like a header (mostly by itself on a line)
                    line_start = text.rfind('\n', 0, match.start()) + 1
                    line_end = text.find('\n', match.end())
                    if line_end == -1:
                        line_end = len(text)
                    
                    line_text = text[line_start:line_end].strip()
                    # If the match makes up most of the line, treat as header
                    if len(match.group()) >= len(line_text) * 0.5:
                        found_headers.append({
                            "name": sec_name,
                            "risk_level": sec_data["risk_level"],
                            "pos": match.end()
                        })

        # Sort headers by position
        found_headers.sort(key=lambda x: x["pos"])

        # Create section spans
        for i, header in enumerate(found_headers):
            start = header["pos"]
            end = found_headers[i+1]["pos"] if i + 1 < len(found_headers) else len(text)
            sections.append(DocumentSection(
                name=header["name"],
                risk_level=header["risk_level"],
                start=start,
                end=end
            ))

        return sections
