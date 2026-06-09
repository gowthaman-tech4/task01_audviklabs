import urllib.request
import json
from typing import List
from .detectors.base import PIIEntity
from .classifier import DocumentType

class LLMVerifier:
    """
    Routes uncertain entities to a local LLM (Ollama) for contextual reasoning.
    """

    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        self.enabled = True
        
        # Test if Ollama is running
        try:
            req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status != 200:
                    self.enabled = False
        except Exception:
            print("[WARN] Ollama not detected at localhost:11434. LLM Verifier disabled.")
            self.enabled = False

    def verify(self, entities: List[PIIEntity], text: str, doc_type: DocumentType) -> List[PIIEntity]:
        if not self.enabled:
            # If disabled, fallback REVIEW items to AUTO_MASK for safety
            for ent in entities:
                if ent.decision == "REVIEW":
                    ent.decision = "AUTO_MASK"
                    ent.reason += " (Fallback: LLM offline)"
            return entities

        from .detectors.base import PIIType
        for ent in entities:
            if ent.decision != "REVIEW":
                continue

            # Only send PERSON_NAME, ORGANIZATION, and ADDRESS (LOCATION) to LLM
            if ent.pii_type not in [PIIType.PERSON_NAME, PIIType.ORGANIZATION, PIIType.ADDRESS]:
                if ent.risk_score >= 0.50:
                    ent.decision = "AUTO_MASK"
                    ent.reason += " (Bypassed LLM: Structured entity auto-masked)"
                else:
                    ent.decision = "AUTO_KEEP"
                    ent.reason += " (Bypassed LLM: Structured entity auto-kept)"
                continue

            window_start = max(0, ent.start - 80)
            window_end = min(len(text), ent.end + 80)
            context = text[window_start:window_end].replace('\n', ' ')

            prompt = f"""You are an Enterprise Privacy Decision Engine.

Your responsibility is NOT to identify entities. Entity detection has already been completed.
Your responsibility is to determine whether a detected entity should be redacted from a document.

==== ENTITY UNDER REVIEW ====
Document Type: {doc_type.value}
Entity Value: "{ent.value}"
Detected Type: {ent.pii_type.value}
Context Snippet: "...{context}..."
=============================

Core Principle:
An entity must only be redacted if it can directly or indirectly identify a specific individual, customer, patient, applicant, taxpayer, account holder, policy holder, borrower, employee, or beneficiary.

Decision Categories:
1. MASK
2. KEEP

Always MASK:
* Person Names belonging to customers, applicants, account holders, taxpayers, patients, employees, policy holders, borrowers, beneficiaries, or individuals
* Email Addresses, Phone Numbers, Aadhaar Numbers, PAN Numbers, Passport Numbers, Driving License Numbers
* Credit Card Numbers, Debit Card Numbers, Bank Account Numbers
* Customer IDs, Loan IDs, Policy Numbers, Tax IDs, Medical Record Numbers
* Full Residential Addresses, Postal Codes / PIN Codes, Dates of Birth
* Any unique identifier associated with an individual

Always KEEP:
* Employer Names, Bank Names, Government Department Names, Public Institution Names, Hospital Names, Company Names
* Form Titles, Section Headers, Document Metadata, Generic Financial Terms, Tax Categories
* State Names, City Names, Country Names, Public Branch Names
* IFSC Codes unless policy explicitly requires masking

Context Rules:
* If a PERSON entity appears near: Name, Customer Name, Applicant, Beneficiary, Account Holder, Policy Holder, Borrower, Patient, Employee Name -> classify as MASK.
* If an ORGANIZATION entity appears near: Employer, Company, Bank, Deductor, Institution, Hospital -> classify as KEEP unless it directly identifies a private individual.
* If an ADDRESS entity consists only of: City, State, Country -> classify as KEEP.
* If an ADDRESS entity contains: House Number, Street, Road, Lane, Apartment, Building, Flat Number, Postal Code, PIN Code -> classify as MASK.

Never mask an entity solely because it was detected by OCR, NER, Regex, LayoutLM, Presidio, or an LLM. Detection is evidence. Context determines redaction. The objective is maximum privacy protection while minimizing unnecessary redaction and preserving document usability.

Decision Requirements:
Output your decision strictly as a JSON object with two keys:
1. "decision": must be either "MASK" or "KEEP"
2. "reason": a brief one sentence explanation citing the context rule used.

Example: {{"decision": "MASK", "reason": "The entity is a person name appearing near 'Account Holder'."}}
"""
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.0
            }

            try:
                import re
                req = urllib.request.Request(self.api_url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    response_text = result.get('response', '').strip()
                    
                    # Try to parse JSON output
                    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                    if json_match:
                        try:
                            llm_json = json.loads(json_match.group(0))
                            decision = llm_json.get("decision", "").upper()
                            reason = llm_json.get("reason", response_text)
                            if "MASK" in decision:
                                ent.decision = "AUTO_MASK"
                                ent.reason = f"LLM Logic: {reason}"
                            elif "KEEP" in decision:
                                ent.decision = "AUTO_KEEP"
                                ent.reason = f"LLM Logic: {reason}"
                            else:
                                ent.decision = "AUTO_MASK"
                                ent.reason += " (LLM failed to provide valid decision)"
                        except json.JSONDecodeError:
                            ent.decision = "AUTO_MASK"
                            ent.reason += " (LLM failed to output valid JSON)"
                    else:
                        # Fallback parsing
                        if "MASK" in response_text.upper():
                            ent.decision = "AUTO_MASK"
                            ent.reason = f"LLM Logic: {response_text}"
                        elif "KEEP" in response_text.upper():
                            ent.decision = "AUTO_KEEP"
                            ent.reason = f"LLM Logic: {response_text}"
                        else:
                            ent.decision = "AUTO_MASK" # Fallback
                            ent.reason += " (LLM failed to format response)"
            except Exception as e:
                print(f"[WARN] LLM verification failed for '{ent.value}': {e}")
                ent.decision = "AUTO_MASK"
                ent.reason += " (Fallback: LLM Error)"

        return entities
