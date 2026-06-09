import re
from typing import List
from .base import PIIDetector, PIIEntity, PIIType

try:
    from presidio_analyzer import AnalyzerEngine, RecognizerResult, PatternRecognizer, Pattern
except ImportError:
    AnalyzerEngine = None

class PresidioDetector(PIIDetector):
    """Detects PII entities using Microsoft Presidio."""

    PRESIDIO_TO_PII_MAP = {
        "PERSON": PIIType.PERSON_NAME,
        "EMAIL_ADDRESS": PIIType.EMAIL,
        "PHONE_NUMBER": PIIType.PHONE,
        "CREDIT_CARD": PIIType.CREDIT_CARD,
        "US_SSN": PIIType.SSN,
        "LOCATION": PIIType.ADDRESS,
        "ORGANIZATION": PIIType.ORGANIZATION,
        "DATE_TIME": PIIType.DATE_OF_BIRTH,
        "IN_PAN": PIIType.PAN,
        "IN_AADHAAR": PIIType.AADHAAR,
        "IN_IFSC": PIIType.IFSC_CODE,
        "IN_CIN": PIIType.COMPANY_ID,
        "IN_VOTER": PIIType.VOTER_ID,
        "IN_DL": PIIType.DRIVING_LICENSE,
        "ACCOUNT_NUM": PIIType.ACCOUNT_NUMBER,
        "PASSPORT_NUM": PIIType.PASSPORT
    }

    def __init__(self, model_name: str = "en_core_web_lg"):
        if AnalyzerEngine is None:
            raise ImportError(
                "presidio-analyzer is required for Presidio detection. "
                "Install it with: pip install presidio-analyzer"
            )
            
        # Initialize Presidio Analyzer with the specified model
        from presidio_analyzer.nlp_engine import NlpEngineProvider
        
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": model_name}]
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()
        
        self._analyzer = AnalyzerEngine(
            supported_languages=["en"],
            nlp_engine=nlp_engine
        )
        
        # Add custom recognizers
        self._add_custom_recognizers()

    @property
    def name(self) -> str:
        return "presidio"

    def _add_custom_recognizers(self):
        # PAN Recognizer
        pan_pattern = Pattern(name="pan_pattern", regex=r'\b[A-Z]{5}\d{4}[A-Z]\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_PAN", patterns=[pan_pattern], context=["pan", "permanent account number"]))

        # Aadhaar Recognizer
        aadhaar_pattern = Pattern(name="aadhaar_pattern", regex=r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_AADHAAR", patterns=[aadhaar_pattern], context=["aadhaar", "aadhar", "uid"]))

        # IFSC Recognizer
        ifsc_pattern = Pattern(name="ifsc_pattern", regex=r'\b[A-Z]{4}0[A-Z0-9]{6}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_IFSC", patterns=[ifsc_pattern], context=["ifsc", "ifs code", "bank branch"]))
        
        # CIN Recognizer
        cin_pattern = Pattern(name="cin_pattern", regex=r'\b[LU]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}\b', score=0.98)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_CIN", patterns=[cin_pattern], context=["cin", "corporate identity number"]))

        # Indian Account Number
        account_pattern = Pattern(name="account_pattern", regex=r'\b\d{6,18}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="ACCOUNT_NUM", patterns=[account_pattern], context=["account", "acct", "a/c"]))
        
        # Indian Mobile Number
        mobile_pattern = Pattern(name="mobile_pattern", regex=r'\b(?:\+?91[\-\s]?)?[6789]\d{9}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_MOBILE", patterns=[mobile_pattern], context=["mobile", "phone", "ph", "cell", "number"]))

        # Indian PIN Code
        pincode_pattern = Pattern(name="pincode_pattern", regex=r'\b\d{6}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_PINCODE", patterns=[pincode_pattern], context=["pin", "pincode", "zip"]))

        # Passport
        passport_pattern = Pattern(name="passport_pattern", regex=r'\b[A-Z]\d{7}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="PASSPORT_NUM", patterns=[passport_pattern], context=["passport", "passport no"]))

        # Loan Number
        loan_pattern = Pattern(name="loan_pattern", regex=r'\b(?:LN|LOAN)[\s\-]*\d{6,10}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="LOAN_NUM", patterns=[loan_pattern], context=["loan"]))

        # Policy Number
        policy_pattern = Pattern(name="policy_pattern", regex=r'\b(?:POL)[\s\-]*\d{6,10}\b', score=0.85)
        self._analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="POLICY_NUM", patterns=[policy_pattern], context=["policy"]))

    def detect(self, text: str) -> List[PIIEntity]:
        """Detect PII entities using Presidio."""
        results: List[RecognizerResult] = self._analyzer.analyze(text=text, language="en", return_decision_process=False)

        entities = []
        for res in results:
            pii_type = self.PRESIDIO_TO_PII_MAP.get(res.entity_type)
            # Handle the newly added custom entities that aren't mapped
            if res.entity_type == "LOAN_NUM": pii_type = PIIType.LOAN_NUMBER
            elif res.entity_type == "POLICY_NUM": pii_type = PIIType.POLICY_NUMBER
            elif res.entity_type == "IN_MOBILE": pii_type = PIIType.PHONE
            elif res.entity_type == "IN_PINCODE": pii_type = PIIType.ADDRESS

            if not pii_type:
                continue

            value = text[res.start:res.end]
            
            if res.score < 0.75:
                continue

            # Skip general dates unless explicitly born/dob
            if pii_type == PIIType.DATE_OF_BIRTH:
                ctx = text[max(0, res.start-40):res.end+20].lower()
                if not any(kw in ctx for kw in ['dob', 'birth', 'born', 'age']):
                    continue

            # Presidio's LOCATION is sometimes very broad. We'll accept it if it's longer than 4 chars
            if pii_type == PIIType.ADDRESS and len(value) <= 4:
                continue
                
            # Filter generic words Presidio mistakes for ORG or PERSON
            val_lower = value.lower().strip()
            if pii_type in (PIIType.ORGANIZATION, PIIType.PERSON_NAME):
                fp_words = [
                    'mobile', 'email', 'phone', 'name', 'date', 'bank', 'customer', 'account', 'statement', 
                    'xyz bank', 'total', 'balance', 'assets', 'liabilities', 'profit', 'loss', 'tax', 
                    'gst', 'rupees', 'amount', 'invoice', 'description', 'quantity', 'rate', 'price',
                    'current', 'non-current', 'equity', 'revenue', 'expenses', 'income', 'branch',
                    'inward', 'outward', 'payment', 'transfer', 'deposit', 'withdrawal', 'interest',
                    'credit', 'debit', 'summary', 'details', 'particulars', 'reference', 'ref', 'no.', 'number'
                ]
                
                # Reject if ANY stop word is entirely inside the value or value is inside stop word
                is_fp = False
                for fp in fp_words:
                    # Check exact match or if the FP word is a standalone word in the value
                    if fp == val_lower or f" {fp} " in f" {val_lower} ":
                        is_fp = True
                        break
                        
                if is_fp or len(val_lower) <= 3:
                    continue

            entities.append(PIIEntity(pii_type=pii_type, value=value, start=res.start, end=res.end, confidence=res.score, source=self.name))

        return entities
