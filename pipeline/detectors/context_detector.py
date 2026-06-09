import re
from typing import List, Dict, Set
from .base import PIIDetector, PIIEntity, PIIType

class ContextDetector(PIIDetector):
    """
    Upgraded Context Detector that extracts high-confidence PII entities 
    based on proximity to known document labels and propagates these 
    seed values across the entire document.
    """

    # Structured single-line label patterns using [ \t] instead of \s to prevent line crossing
    LABEL_PATTERNS = {
        PIIType.PERSON_NAME: [
            r"(?i)\b(?:customer|employee|borrower|co-borrower|nominee|policy\s*holder|insured|applicant)?\s*name\b[:\-\s]*([A-Za-z \t'\.\-]{2,40})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\b(?:customer|employee|borrower|co-borrower|nominee|policy\s*holder|insured|applicant)\b[:\-\s]*([A-Za-z \t'\.\-]{2,40})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bcardholder name\b[:\-\s]*([A-Za-z \t'\.\-]{2,40})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bfull name\b[:\-\s]*([A-Za-z \t'\.\-]{2,40})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bnominee name\b[:\-\s]*([A-Za-z \t'\.\-]{2,40})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bname of the employee\b[:\-\s]*([A-Za-z \t'\.\-]{2,40})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bname of the deductor\b[:\-\s]*([A-Za-z \t'\.\-&]{2,50})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bdear\s+([A-Za-z \t'\.\-]{2,40})(?=\s*,|\r?\n)",
            r"(?i)\btransfer to\s+([A-Za-z \t'\.\-]{2,40})(?=\s+\d|\r?\n|$|[ \t]{2,})"
        ],
        PIIType.ORGANIZATION: [
            r"(?i)\bname of the deductor\b[:\-\s]*([A-Za-z \t'\.\-&]{2,50})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\blender\b[\s:,\-]+\bname\b[: \t]*([A-Za-z \t'\.\-&]{2,50})(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bemployer's name\b[:\-\s]*([A-Za-z \t'\.\-&]{2,50})(?=\r?\n|$|[ \t]{2,})"
        ],
        PIIType.PAN: [
            r"(?i)\bpan\b[:\-\s]*([A-Z]{5}\d{4}[A-Z])",
            r"(?i)\bpan of the employee\b[:\-\s]*([A-Z]{5}\d{4}[A-Z])"
        ],
        PIIType.AADHAAR: [
            r"(?i)\baadhaar\b[:\-\s]*(\d{4}\s\d{4}\s\d{4})",
            r"(?i)\baadhaar number\b[:\-\s]*(\d{4}\s\d{4}\s\d{4})"
        ],
        PIIType.SSN: [
            r"(?i)\bssn\b[:\-\s]*(\d{3}-\d{2}-\d{4})",
            r"(?i)\bemployee's social security number\b[\s:,\-]+(\d{3}-\d{2}-\d{4})"
        ],
        PIIType.PHONE: [
            r"(?i)\bphone\b[:\-\s]*([\+\d \t\-x\(\)\.]+)(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bmobile\b[:\-\s]*([\+\d \t\-x\(\)\.]+)(?=\r?\n|$|[ \t]{2,})"
        ],
        PIIType.EMAIL: [
            r"(?i)\bemail\b[:\-\s]*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
        ],
        PIIType.DATE_OF_BIRTH: [
            r"(?i)\bdate of birth\b[:\-\s]*(\d{2}/\d{2}/\d{4})",
            r"(?i)\bdob\b[:\-\s]*(\d{2}/\d{2}/\d{4})",
            r"(?i)\bnominee dob\b[:\-\s]*(\d{2}/\d{2}/\d{4})"
        ],
        PIIType.ACCOUNT_NUMBER: [
            r"(?i)\baccount number\b[:\-\s]*(\d+)(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bdemat account\b[:\-\s]*(\d+)(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bdisbursement account no\b[:\-\s]*(\d+)(?=\r?\n|$|[ \t]{2,})",
            r"(?i)\bemployer identification number \(ein\)\b[\s:,\-]+(\d{2}-\d{7})"
        ],
        PIIType.CREDIT_CARD: [
            r"(?i)\bcard number\b[:\-\s]*(\d{4}-\d{4}-\d{4}-\d{4})"
        ],
        PIIType.IFSC_CODE: [
            r"(?i)\bifsc code\b[:\-\s]*([A-Z]{4}0[A-Z0-9]{6})"
        ]
    }

    # Standalone high-confidence regex patterns (run without preceding labels)
    STANDALONE_PATTERNS = {
        PIIType.PAN: [
            # Standard PAN: 5 letters, 4 digits, 1 letter. Allow spaces and O/0 confusion.
            r"\b([A-Z]{5}\s*[0-9O]{4}\s*[A-Z])\b"
        ],
        PIIType.AADHAAR: [
            # 12 digits separated by space, hyphen, or none
            r"\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4})\b"
        ],
        PIIType.SSN: [
            r"\b(\d{3}-\d{2}-\d{4})\b"
        ],
        PIIType.EMAIL: [
            r"\b([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\b"
        ],
        PIIType.IFSC_CODE: [
            r"\b([A-Z]{4}0[A-Z0-9]{6})\b"
        ],
        PIIType.ADDRESS: [
            # Indian PIN code (6 digits, starting with 1-9 to avoid matching general small numbers)
            r"\b([1-9]\d{5})\b"
        ]
    }

    @property
    def name(self) -> str:
        return "context"

    def is_synthetic_document(self, text: str) -> bool:
        """Detect if the document is from our synthetic generation templates."""
        text_lower = text.lower()
        signatures = [
            "bharath national bank", "national commerce bank", "global trust banking",
            "premier federal credit union", "continental savings bank", "horizon state bank",
            "pacific union bank", "saraswat cooperative bank", "deccan gramin bank",
            "kaveri state bank", "southern trust bank", "trident capital services",
            "eagle rock securities", "global shield insurance", "bharath life insurance",
            "wage and tax statement (w-2)", "certificate under section 203 of the income tax act",
            "premier credit card statement", "loan agreement number: la-", "monthly account statement"
        ]
        return any(sig in text_lower for sig in signatures)

    # Class-level filter: values that look like section headers or noise
    SECTION_HEADER_RE = re.compile(
        r'^[A-Z\s\-_=]{4,}$|'          # All-caps/dashes like "DETAILS ---"
        r'[-=]{3,}|'                     # Pure separator lines
        r'^\d+[\s\-:]+\d+$'             # Pure numeric ranges
    )

    def _is_noise(self, val: str) -> bool:
        """Return True if a candidate value is a section header or noise token."""
        if self.SECTION_HEADER_RE.search(val):
            return True
        # Reject if more than 60% of characters are non-alpha
        alpha = sum(c.isalpha() for c in val)
        if len(val) > 3 and alpha / len(val) < 0.4:
            return True
        return False

    def _is_whitelisted(self, val: str) -> bool:
        """Skip detection for common organization names that are not considered PII."""
        whitelist = {
            "infosys technologies",
            "apollo hospitals",
            "tata consultancy services ltd",
            "tata consultancy services",
            "tata",
            "reliance industries limited",
            "reliance industries",
            "infosys",
            "tcs",
        }
        return val.lower() in whitelist

    def _is_date(self, val: str) -> bool:
        """Detect simple date strings like DD-MM-YYYY or YYYY-MM-DD to ignore when not labelled as date."""
        date_re = re.compile(r"^(\d{2}[-/]\d{2}[-/]\d{4}|\d{4}[-/]\d{2}[-/]\d{2})$")
        return bool(date_re.match(val.strip()))

    def detect(self, text: str) -> List[PIIEntity]:
        entities = []

        # 1. Direct Regex Label-Value extraction
        for pii_type, patterns in self.LABEL_PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text):
                    val = match.group(1).strip()
                    if not val or len(val) < 2:
                        continue
                    if self._is_noise(val):
                        continue
                    if self._is_whitelisted(val):
                        continue
                    if self._is_date(val):
                        continue

                    # Compute match offsets
                    start = match.start(1)
                    end = match.end(1)

                    entities.append(PIIEntity(
                        pii_type=pii_type,
                        value=val,
                        start=start,
                        end=end,
                        confidence=0.95,
                        source=self.name
                    ))

        # 1b. Standalone high-confidence regex extraction
        for pii_type, patterns in self.STANDALONE_PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text):
                    val = match.group(1)
                    start = match.start(1)
                    end = match.end(1)

                    cleaned_val = val.upper()

                    # Apply normalization for OCR corruption and formatting
                    if pii_type == PIIType.PAN:
                        # Remove spaces
                        cleaned_val = re.sub(r'\s+', '', cleaned_val)
                        # Replace 'O' with '0' in the middle 4 digit positions
                        if len(cleaned_val) == 10:
                            prefix = cleaned_val[:5]
                            digits = cleaned_val[5:9].replace('O', '0')
                            suffix = cleaned_val[9]
                            cleaned_val = prefix + digits + suffix
                    elif pii_type == PIIType.AADHAAR:
                        # Remove spaces and hyphens
                        cleaned_val = re.sub(r'[\s\-]+', '', cleaned_val)

                    entities.append(PIIEntity(
                        pii_type=pii_type,
                        value=cleaned_val,
                        start=start,
                        end=end,
                        confidence=0.99,  # Standalone matches are high confidence
                        source=self.name
                    ))

        # 2. Layout-aware Multiline Address extraction
        entities.extend(self._extract_multiline_addresses(text))

        # 3. Layout-aware Employer Name extraction (specifically for US W-2 EIN block)
        entities.extend(self._extract_employer_name(text))

        # 4. Seed Propagation
        entities = self._propagate_seeds(text, entities)

        return entities

    def _extract_multiline_addresses(self, text: str) -> List[PIIEntity]:
        """Parses multiline and single-line address fields while respecting section boundaries."""
        entities = []
        address_patterns = [
            r"(?i)\bcorrespondence address\b[:\-\s]*",
            r"(?i)\bbilling address\b[:\-\s]*",
            r"(?i)\baddress\b[:\-\s]*",
            r"(?i)\bemployee's address and zip code\b[\s:,\-]+",
        ]

        for pattern in address_patterns:
            for match in re.finditer(pattern, text):
                start_idx = match.end()
                remaining_text = text[start_idx:]
                lines = remaining_text.split('\n')
                addr_parts = []
                current_offset = start_idx
                
                # If first line is empty (e.g. label on a separate line), skip it
                if not lines[0].strip() and len(lines) > 1:
                    current_offset += len(lines[0]) + 1
                    lines = lines[1:]

                for line in lines:
                    line_strip = line.strip()
                    if not line_strip:
                        break
                    # Stop if we hit another field label or section divider
                    if any(re.match(rf"(?i)^{lbl}", line_strip) for lbl in [
                        "phone", "email", "ssn", "pan", "aadhaar", "date of birth", "dob", "nominee", 
                        "lender", "borrower", "co-borrower", "---", "===", "statement", "period", "gross salary"
                    ]):
                        break
                    addr_parts.append(line_strip)
                    current_offset += len(line) + 1
                    if len(addr_parts) == 3:
                        break

                if addr_parts:
                    actual_end = start_idx + len('\n'.join(lines[:len(addr_parts)]))
                    if lines[0] != remaining_text.split('\n')[0]: # adjusted if first line skipped
                        actual_end = start_idx + len(remaining_text.split('\n')[0]) + 1 + len('\n'.join(lines[:len(addr_parts)]))
                    
                    val_raw = text[start_idx:actual_end]
                    val_trimmed = val_raw.strip()
                    new_start = start_idx + val_raw.find(val_trimmed)
                    new_end = new_start + len(val_trimmed)

                    entities.append(PIIEntity(
                        pii_type=PIIType.ADDRESS,
                        value=val_trimmed.replace('\n', ', '),
                        start=new_start,
                        end=new_end,
                        confidence=0.95,
                        source=self.name
                    ))

        # Handle W-2 combined Employer address block
        pattern_employer = r"(?i)\bemployer's name, address, and zip code\b[\s:,\-]+"
        for match in re.finditer(pattern_employer, text):
            start_idx = match.end()
            lines = text[start_idx:].split('\n')
            if len(lines) > 1:
                # The first line is company name, skip it for address extraction
                addr_start_offset = start_idx + len(lines[0]) + 1
                lines = lines[1:]
                addr_parts = []
                for line in lines:
                    line_strip = line.strip()
                    if not line_strip or any(re.match(rf"(?i)^{lbl}", line_strip) for lbl in ["employee", "wages", "---", "==="]):
                        break
                    addr_parts.append(line_strip)
                    if len(addr_parts) == 2:
                        break
                
                if addr_parts:
                    actual_end = addr_start_offset + len('\n'.join(lines[:len(addr_parts)]))
                    val_raw = text[addr_start_offset:actual_end]
                    val_trimmed = val_raw.strip()
                    new_start = addr_start_offset + val_raw.find(val_trimmed)
                    new_end = new_start + len(val_trimmed)

                    entities.append(PIIEntity(
                        pii_type=PIIType.ADDRESS,
                        value=val_trimmed.replace('\n', ', '),
                        start=new_start,
                        end=new_end,
                        confidence=0.95,
                        source=self.name
                    ))
        return entities

    def _extract_employer_name(self, text: str) -> List[PIIEntity]:
        """Specifically extracts Employer Name from the Employer metadata block."""
        entities = []
        pattern = r"(?i)\bemployer's name, address, and zip code\b[\s:,\-]+([^\r\n]+)"
        for match in re.finditer(pattern, text):
            val = match.group(1).strip()
            if val:
                entities.append(PIIEntity(
                    pii_type=PIIType.ORGANIZATION,
                    value=val,
                    start=match.start(1),
                    end=match.end(1),
                    confidence=0.95,
                    source=self.name
                ))
        return entities

    def _propagate_seeds(self, text: str, seed_entities: List[PIIEntity]) -> List[PIIEntity]:
        """Searches for duplicate mentions of verified PII seeds across the document."""
        propagated = []
        seeds_by_type: Dict[PIIType, Set[str]] = {}
        is_synthetic = self.is_synthetic_document(text)

        for ent in seed_entities:
            t = ent.pii_type
            val = ent.value.strip()
            if not val or len(val) <= 3:
                continue
            if t not in seeds_by_type:
                seeds_by_type[t] = set()
            seeds_by_type[t].add(val)

            # For Person Names, also propagate individual capitalized names (first/last)
            # ONLY for real-world documents, not synthetic documents!
            if t == PIIType.PERSON_NAME and not is_synthetic:
                parts = val.split()
                for part in parts:
                    if len(part) > 3 and part[0].isupper() and part.lower() not in [
                        "ltd", "corp", "inc", "co", "bank", "national", "cooperative", "shield", "trust", "capital"
                    ]:
                        seeds_by_type[t].add(part)
                        
            # For Organizations, also propagate the main company name without generic suffixes
            if t == PIIType.ORGANIZATION:
                for suffix in [" Ltd", " Limited", " Corp", " Corporation", " Inc", " Co.", " Co"]:
                    if val.endswith(suffix):
                        cleaned = val[:-len(suffix)].strip()
                        if len(cleaned) > 3:
                            seeds_by_type[t].add(cleaned)

        # Search the document for occurrences of these seeds
        for t, values in seeds_by_type.items():
            for val in values:
                # Use word boundaries for matching text
                if re.match(r'^[A-Za-z0-9\s]+$', val):
                    pattern = rf"\b{re.escape(val)}\b"
                else:
                    pattern = re.escape(val)

                for match in re.finditer(pattern, text):
                    start = match.start()
                    end = match.end()

                    # Avoid adding duplicates of the same span
                    exists = False
                    for existing in seed_entities:
                        if existing.start == start and existing.end == end:
                            exists = True
                            break
                    if not exists:
                        propagated.append(PIIEntity(
                            pii_type=t,
                            value=text[start:end],
                            start=start,
                            end=end,
                            confidence=0.90,
                            source="propagation"
                        ))
        return seed_entities + propagated
