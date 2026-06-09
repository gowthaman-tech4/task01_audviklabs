from enum import Enum

class DocumentType(Enum):
    BANK_STATEMENT = "BANK_STATEMENT"
    TAX_RETURN = "TAX_RETURN"
    LOAN_DOCUMENT = "LOAN_DOCUMENT"
    INSURANCE = "INSURANCE"
    BROKERAGE_STATEMENT = "BROKERAGE_STATEMENT"
    CREDIT_CARD_STATEMENT = "CREDIT_CARD_STATEMENT"
    MEDICAL_RECORD = "MEDICAL_RECORD"
    GENERIC = "GENERIC"

class DocumentClassifier:
    """Classifies documents into types based on keyword signatures."""

    def classify(self, text: str) -> DocumentType:
        if not text:
            return DocumentType.GENERIC
            
        text_lower = text.lower()

        # 1. Credit Card Statement
        if "credit card statement" in text_lower or "premier credit card" in text_lower or "cardholder name:" in text_lower:
            return DocumentType.CREDIT_CARD_STATEMENT

        # 2. Bank Statement
        if "monthly account statement" in text_lower or ("account summary" in text_lower and "transaction details" in text_lower):
            return DocumentType.BANK_STATEMENT

        # 3. Tax Return (W-2 or Form 16)
        if "wage and tax statement" in text_lower or "w-2" in text_lower or "form 16" in text_lower or "assessment year:" in text_lower or "tan of the deductor" in text_lower:
            return DocumentType.TAX_RETURN

        # 4. Loan Agreement
        if "loan agreement" in text_lower or "loan tenure" in text_lower or "borrower:" in text_lower or "lender:" in text_lower or "disbursement account" in text_lower:
            return DocumentType.LOAN_DOCUMENT

        # 5. Insurance Letter
        if "policy document" in text_lower or "certificate of insurance" in text_lower or "shield insurance" in text_lower or "life insurance" in text_lower or "nominee name" in text_lower:
            return DocumentType.INSURANCE

        # 6. Brokerage Statement
        if "investment statement" in text_lower or "portfolio holdings" in text_lower or "trident capital" in text_lower or "eagle rock" in text_lower or "demat account" in text_lower:
            return DocumentType.BROKERAGE_STATEMENT

        return DocumentType.GENERIC
