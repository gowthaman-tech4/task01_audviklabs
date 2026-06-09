"""
Synthetic financial document generator with PII ground truth.

Generates realistic-looking financial documents (bank statements, tax forms,
loan agreements, insurance letters, brokerage reports) containing known PII
entities with their exact positions tracked for evaluation.
"""
import os
import json
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from faker import Faker
from faker.providers import BaseProvider


# Initialize Faker with both US and Indian locales
fake_us = Faker('en_US')
fake_in = Faker('en_IN')
Faker.seed(42)
random.seed(42)


class IndianPIIProvider(BaseProvider):
    """Custom Faker provider for Indian PII data."""

    def pan_number(self) -> str:
        """Generate a realistic Indian PAN number."""
        letters = string.ascii_uppercase
        # PAN format: AAAAA9999A
        # 4th char indicates holder type: P=Person, C=Company, etc.
        first_three = ''.join(random.choices(letters, k=3))
        fourth = random.choice('PCHABGJLFT')
        fifth = random.choice(letters)
        digits = ''.join(random.choices(string.digits, k=4))
        last = random.choice(letters)
        return f"{first_three}{fourth}{fifth}{digits}{last}"

    def aadhaar_number(self) -> str:
        """Generate a realistic Aadhaar number (12 digits, not starting with 0 or 1)."""
        first = str(random.randint(2, 9))
        rest = ''.join(random.choices(string.digits, k=11))
        digits = first + rest
        return f"{digits[:4]} {digits[4:8]} {digits[8:12]}"

    def ifsc_code(self) -> str:
        """Generate a realistic IFSC code."""
        bank_codes = ['SBIN', 'HDFC', 'ICIC', 'AXIS', 'PUNB', 'BARB',
                      'UBIN', 'CNRB', 'IOBA', 'BKID']
        bank = random.choice(bank_codes)
        branch = ''.join(random.choices(string.digits, k=6))
        return f"{bank}0{branch}"

    def indian_phone(self) -> str:
        """Generate an Indian phone number."""
        prefix = random.choice(['91', '+91'])
        # Indian mobile numbers start with 6-9
        first = str(random.randint(6, 9))
        rest = ''.join(random.choices(string.digits, k=9))
        number = first + rest
        return f"{prefix} {number[:5]} {number[5:]}"

    def indian_account_number(self) -> str:
        """Generate a bank account number (10-16 digits)."""
        length = random.randint(10, 16)
        return ''.join(random.choices(string.digits, k=length))


# Register custom provider
fake_in.add_provider(IndianPIIProvider)


class PIITracker:
    """
    Tracks PII entities and their positions in generated text.
    Builds ground truth for evaluation.
    """

    def __init__(self):
        self.entities: List[Dict] = []
        self._text_parts: List[str] = []
        self._current_pos: int = 0

    def add_text(self, text: str):
        """Add non-PII text."""
        self._text_parts.append(text)
        self._current_pos += len(text)

    def add_pii(self, value: str, pii_type: str) -> str:
        """Add a PII value and track its position."""
        start = self._current_pos
        end = start + len(value)

        self.entities.append({
            "type": pii_type,
            "value": value,
            "start": start,
            "end": end
        })

        self._text_parts.append(value)
        self._current_pos = end
        return value

    def get_text(self) -> str:
        """Get the full generated text."""
        return ''.join(self._text_parts)

    def get_ground_truth(self) -> List[Dict]:
        """Get the ground truth entity list."""
        return self.entities

    def reset(self):
        """Reset tracker for a new document."""
        self.entities = []
        self._text_parts = []
        self._current_pos = 0


def generate_bank_statement(locale: str = "us") -> Tuple[str, List[Dict]]:
    """Generate a synthetic bank statement."""
    tracker = PIITracker()
    fake = fake_us if locale == "us" else fake_in

    # Header
    bank_name = random.choice([
        "National Commerce Bank", "Global Trust Banking Corp",
        "Premier Federal Credit Union", "Continental Savings Bank",
        "Horizon State Bank", "Pacific Union Bank"
    ]) if locale == "us" else random.choice([
        "Bharath National Bank", "Saraswat Cooperative Bank",
        "Deccan Gramin Bank", "Kaveri State Bank",
        "Peninsula Banking Corporation", "Southern Trust Bank Ltd"
    ])

    tracker.add_text(f"""{'='*60}
                    {bank_name}
                  MONTHLY ACCOUNT STATEMENT
{'='*60}

Statement Period: {fake.date_between('-60d', '-30d').strftime('%B %d, %Y')} to {fake.date_between('-29d', 'today').strftime('%B %d, %Y')}
Statement Date: {datetime.now().strftime('%B %d, %Y')}

--- ACCOUNT HOLDER INFORMATION ---

Name:              """)
    tracker.add_pii(fake.name(), "PERSON_NAME")

    tracker.add_text("\nAccount Number:    ")
    acct = fake_in.indian_account_number() if locale == "in" else ''.join(random.choices(string.digits, k=12))
    tracker.add_pii(acct, "ACCOUNT_NUMBER")

    if locale == "in":
        tracker.add_text("\nIFSC Code:         ")
        tracker.add_pii(fake_in.ifsc_code(), "IFSC_CODE")

        tracker.add_text("\nPAN:               ")
        tracker.add_pii(fake_in.pan_number(), "PAN")
    else:
        tracker.add_text("\nSSN:               ")
        # Generate valid SSN
        area = random.randint(100, 665)
        group = random.randint(1, 99)
        serial = random.randint(1, 9999)
        tracker.add_pii(f"{area:03d}-{group:02d}-{serial:04d}", "SSN")

    tracker.add_text("\nPhone:             ")
    phone = fake_in.indian_phone() if locale == "in" else fake_us.phone_number()
    tracker.add_pii(phone, "PHONE")

    tracker.add_text("\nEmail:             ")
    tracker.add_pii(fake.email(), "EMAIL")

    tracker.add_text("\nDate of Birth:     ")
    dob = fake.date_of_birth(minimum_age=21, maximum_age=70)
    tracker.add_pii(dob.strftime('%m/%d/%Y'), "DATE_OF_BIRTH")

    tracker.add_text("\nAddress:           ")
    addr = fake.address().replace('\n', ', ')
    tracker.add_pii(addr, "ADDRESS")

    # Account summary
    opening_bal = round(random.uniform(5000, 150000), 2)
    num_transactions = random.randint(8, 20)

    tracker.add_text(f"""

--- ACCOUNT SUMMARY ---

Account Type:      {'Savings' if random.random() > 0.5 else 'Checking'} Account
Branch:            {fake.city()} Branch
Opening Balance:   ${opening_bal:,.2f}
""")

    # Transactions
    tracker.add_text(f"""
--- TRANSACTION DETAILS ---

{'Date':<14} {'Description':<35} {'Debit':>12} {'Credit':>12} {'Balance':>14}
{'-'*87}
""")

    balance = opening_bal
    for i in range(num_transactions):
        tx_date = fake.date_between('-30d', 'today').strftime('%m/%d/%Y')
        is_debit = random.random() > 0.4
        amount = round(random.uniform(10, 5000), 2)

        descriptions = [
            f"ATM Withdrawal - {fake.city()}",
            f"Online Transfer to {''.join(random.choices(string.digits, k=8))}",
            f"POS Purchase - {fake.company()[:25]}",
            f"Direct Deposit - {''.join(random.choices(string.ascii_uppercase, k=3))} Corp",
            f"Bill Payment - Utility",
            f"UPI Transfer",
            f"NEFT Transfer",
            f"Check #{random.randint(1000, 9999)}",
            f"Interest Credit",
            f"Service Charge",
        ]
        desc = random.choice(descriptions)

        if is_debit:
            balance -= amount
            tracker.add_text(f"{tx_date:<14} {desc:<35} {amount:>12,.2f} {'':>12} {balance:>14,.2f}\n")
        else:
            balance += amount
            tracker.add_text(f"{tx_date:<14} {desc:<35} {'':>12} {amount:>12,.2f} {balance:>14,.2f}\n")

    tracker.add_text(f"""
{'-'*87}
Closing Balance:   ${balance:,.2f}

--- IMPORTANT NOTICE ---
This is a computer-generated statement and does not require a signature.
For any discrepancies, please contact our customer service at 1-800-555-0199.
This statement is confidential and intended solely for the account holder.

{bank_name}
FDIC Insured | Equal Opportunity Lender
{'='*60}
""")

    return tracker.get_text(), tracker.get_ground_truth()


def generate_tax_form(locale: str = "us") -> Tuple[str, List[Dict]]:
    """Generate a synthetic tax form (W-2 style for US, Form 16 style for India)."""
    tracker = PIITracker()
    fake = fake_us if locale == "us" else fake_in

    if locale == "us":
        # W-2 style
        tracker.add_text(f"""{'='*60}
              WAGE AND TAX STATEMENT (W-2)
                    Tax Year 2025
{'='*60}

a  Employee's Social Security Number
   """)
        area = random.randint(100, 665)
        group = random.randint(1, 99)
        serial = random.randint(1, 9999)
        tracker.add_pii(f"{area:03d}-{group:02d}-{serial:04d}", "SSN")

        tracker.add_text("""

b  Employer Identification Number (EIN)
   """)
        tracker.add_pii(f"{random.randint(10,99)}-{random.randint(1000000,9999999)}", "ACCOUNT_NUMBER")

        tracker.add_text("""

c  Employer's Name, Address, and ZIP Code
   """)
        company = fake.company()
        tracker.add_pii(company, "ORGANIZATION")
        tracker.add_text("\n   ")
        tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

        tracker.add_text("""

e  Employee's Name
   """)
        tracker.add_pii(fake.name(), "PERSON_NAME")

        tracker.add_text("""

f  Employee's Address and ZIP Code
   """)
        tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

        wages = round(random.uniform(35000, 250000), 2)
        fed_tax = round(wages * random.uniform(0.15, 0.30), 2)
        ss_wages = min(wages, 160200)
        ss_tax = round(ss_wages * 0.062, 2)
        medicare_wages = wages
        medicare_tax = round(medicare_wages * 0.0145, 2)

        tracker.add_text(f"""

--- WAGE AND TAX DATA ---

1  Wages, tips, other compensation     ${wages:>12,.2f}
2  Federal income tax withheld         ${fed_tax:>12,.2f}
3  Social Security wages               ${ss_wages:>12,.2f}
4  Social Security tax withheld        ${ss_tax:>12,.2f}
5  Medicare wages and tips             ${medicare_wages:>12,.2f}
6  Medicare tax withheld               ${medicare_tax:>12,.2f}

12a Code DD - Health Insurance          ${round(random.uniform(3000, 15000), 2):>12,.2f}

--- STATE TAX INFORMATION ---

15 State: {fake.state_abbr()}
16 State wages                         ${wages:>12,.2f}
17 State income tax                    ${round(wages * random.uniform(0.03, 0.09), 2):>12,.2f}

{'='*60}
""")

    else:
        # Form 16 style (India)
        tracker.add_text(f"""{'='*60}
              FORM 16 - CERTIFICATE UNDER
         SECTION 203 OF THE INCOME TAX ACT, 1961
                FOR TAX DEDUCTED AT SOURCE
              Assessment Year: 2025-2026
{'='*60}

--- EMPLOYER DETAILS ---

Name of the Deductor:   """)
        tracker.add_pii(fake.company(), "ORGANIZATION")

        tracker.add_text("\nTAN of the Deductor:    ")
        tan = ''.join(random.choices(string.ascii_uppercase, k=4)) + \
              ''.join(random.choices(string.digits, k=5)) + \
              random.choice(string.ascii_uppercase)
        tracker.add_text(tan)

        tracker.add_text("\nAddress:                ")
        tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

        tracker.add_text("""

--- EMPLOYEE DETAILS ---

Name of the Employee:   """)
        tracker.add_pii(fake.name(), "PERSON_NAME")

        tracker.add_text("\nPAN of the Employee:    ")
        tracker.add_pii(fake_in.pan_number(), "PAN")

        tracker.add_text("\nAadhaar Number:         ")
        tracker.add_pii(fake_in.aadhaar_number(), "AADHAAR")

        tracker.add_text("\nDate of Birth:          ")
        dob = fake.date_of_birth(minimum_age=21, maximum_age=60)
        tracker.add_pii(dob.strftime('%d/%m/%Y'), "DATE_OF_BIRTH")

        tracker.add_text("\nAddress:                ")
        tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

        tracker.add_text("\nEmail:                  ")
        tracker.add_pii(fake.email(), "EMAIL")

        tracker.add_text("\nMobile:                 ")
        tracker.add_pii(fake_in.indian_phone(), "PHONE")

        salary = round(random.uniform(300000, 2500000), 2)
        hra = round(salary * 0.4, 2)
        standard_deduction = 50000
        taxable = salary - hra * 0.3 - standard_deduction

        tracker.add_text(f"""

--- SALARY DETAILS ---

1. Gross Salary
   (a) Salary as per Section 17(1)     Rs. {salary:>14,.2f}
   (b) Value of perquisites u/s 17(2)  Rs. {round(random.uniform(0, 50000), 2):>14,.2f}
   (c) Profits in lieu of salary 17(3) Rs.           0.00

2. Less: Exemptions under Section 10
   (a) HRA Exemption                   Rs. {round(hra * 0.3, 2):>14,.2f}
   (b) LTA Exemption                   Rs. {round(random.uniform(0, 30000), 2):>14,.2f}

3. Standard Deduction u/s 16(ia)       Rs. {standard_deduction:>14,.2f}

4. Taxable Income                      Rs. {taxable:>14,.2f}
5. Tax on Total Income                 Rs. {round(taxable * 0.20, 2):>14,.2f}
6. Less: Rebate u/s 87A               Rs.           0.00
7. Education Cess @ 4%                 Rs. {round(taxable * 0.20 * 0.04, 2):>14,.2f}
8. Total Tax Payable                   Rs. {round(taxable * 0.20 * 1.04, 2):>14,.2f}

{'='*60}
""")

    return tracker.get_text(), tracker.get_ground_truth()


def generate_loan_agreement(locale: str = "us") -> Tuple[str, List[Dict]]:
    """Generate a synthetic loan agreement document."""
    tracker = PIITracker()
    fake = fake_us if locale == "us" else fake_in

    loan_amount = round(random.uniform(10000, 500000), 2)
    interest_rate = round(random.uniform(4.5, 18.0), 2)
    tenure_months = random.choice([12, 24, 36, 48, 60, 72, 84, 120, 180, 240])

    tracker.add_text(f"""{'='*60}
                 LOAN AGREEMENT
           PERSONAL / HOME LOAN DOCUMENT
{'='*60}

Loan Agreement Number: LA-{random.randint(100000, 999999)}
Date of Agreement: {fake.date_between('-90d', 'today').strftime('%B %d, %Y')}

This Loan Agreement ("Agreement") is entered into between:

LENDER:
Name: """)
    lender = random.choice(["First National Lending Corp", "Premier Home Finance Ltd",
                            "Continental Credit Corporation", "Bharat Housing Finance Ltd"])
    tracker.add_pii(lender, "ORGANIZATION")
    tracker.add_text("\nAddress: ")
    tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

    tracker.add_text("""

BORROWER:
Name: """)
    tracker.add_pii(fake.name(), "PERSON_NAME")

    if locale == "in":
        tracker.add_text("\nPAN: ")
        tracker.add_pii(fake_in.pan_number(), "PAN")
        tracker.add_text("\nAadhaar: ")
        tracker.add_pii(fake_in.aadhaar_number(), "AADHAAR")
    else:
        tracker.add_text("\nSSN: ")
        area = random.randint(100, 665)
        group = random.randint(1, 99)
        serial = random.randint(1, 9999)
        tracker.add_pii(f"{area:03d}-{group:02d}-{serial:04d}", "SSN")

    tracker.add_text("\nDate of Birth: ")
    dob = fake.date_of_birth(minimum_age=21, maximum_age=65)
    tracker.add_pii(dob.strftime('%m/%d/%Y'), "DATE_OF_BIRTH")

    tracker.add_text("\nAddress: ")
    tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

    tracker.add_text("\nPhone: ")
    phone = fake_in.indian_phone() if locale == "in" else fake_us.phone_number()
    tracker.add_pii(phone, "PHONE")

    tracker.add_text("\nEmail: ")
    tracker.add_pii(fake.email(), "EMAIL")

    # Co-borrower (50% chance)
    if random.random() > 0.5:
        tracker.add_text("""

CO-BORROWER (if applicable):
Name: """)
        tracker.add_pii(fake.name(), "PERSON_NAME")
        tracker.add_text("\nPhone: ")
        phone2 = fake_in.indian_phone() if locale == "in" else fake_us.phone_number()
        tracker.add_pii(phone2, "PHONE")
        tracker.add_text("\nEmail: ")
        tracker.add_pii(fake.email(), "EMAIL")

    emi = round((loan_amount * interest_rate/100/12 *
                 (1 + interest_rate/100/12)**tenure_months) /
                ((1 + interest_rate/100/12)**tenure_months - 1), 2)

    tracker.add_text(f"""

--- LOAN DETAILS ---

Loan Type:                  {'Home Loan' if loan_amount > 100000 else 'Personal Loan'}
Loan Amount:                ${loan_amount:>14,.2f}
Interest Rate:              {interest_rate}% per annum
Loan Tenure:                {tenure_months} months
EMI Amount:                 ${emi:>14,.2f}
Disbursement Account No:    """)
    tracker.add_pii(''.join(random.choices(string.digits, k=14)), "ACCOUNT_NUMBER")

    tracker.add_text(f"""
Disbursement Date:          {fake.date_between('-30d', 'today').strftime('%B %d, %Y')}

--- TERMS AND CONDITIONS ---

1. The Borrower agrees to repay the loan amount along with interest
   in {tenure_months} equal monthly installments of ${emi:,.2f}.
2. Late payment will attract a penalty of 2% per month on the overdue amount.
3. Pre-payment is allowed after 6 months with a foreclosure charge of 3%.
4. The Borrower authorizes the Lender to report loan status to credit bureaus.
5. In case of default, the Lender reserves the right to initiate recovery
   proceedings as per applicable law.

--- DECLARATION ---

I hereby declare that all information provided above is true and correct
to the best of my knowledge. I understand and agree to the terms and
conditions of this loan agreement.

Borrower Signature: ___________________     Date: _______________
Lender Representative: ________________     Date: _______________

{'='*60}
""")

    return tracker.get_text(), tracker.get_ground_truth()


def generate_insurance_letter(locale: str = "us") -> Tuple[str, List[Dict]]:
    """Generate a synthetic insurance policy letter."""
    tracker = PIITracker()
    fake = fake_us if locale == "us" else fake_in

    policy_type = random.choice(["Life", "Health", "Auto", "Home", "Term"])
    premium = round(random.uniform(500, 25000), 2)

    tracker.add_text(f"""{'='*60}
              {'GLOBAL SHIELD INSURANCE CO.' if locale == 'us' else 'BHARATH LIFE INSURANCE LTD.'}
              {'POLICY DOCUMENT / CERTIFICATE OF INSURANCE'}
{'='*60}

Policy Number: POL-{random.randint(1000000, 9999999)}
Policy Type: {policy_type} Insurance
Date of Issue: {fake.date_between('-365d', '-30d').strftime('%B %d, %Y')}

Dear """)
    tracker.add_pii(fake.name(), "PERSON_NAME")

    tracker.add_text(""",

Thank you for choosing our insurance services. Please find below the
details of your insurance policy.

--- POLICYHOLDER DETAILS ---

Full Name:          """)
    tracker.add_pii(fake.name(), "PERSON_NAME")

    tracker.add_text("\nDate of Birth:      ")
    dob = fake.date_of_birth(minimum_age=25, maximum_age=60)
    tracker.add_pii(dob.strftime('%m/%d/%Y'), "DATE_OF_BIRTH")

    tracker.add_text("\nAddress:            ")
    tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

    tracker.add_text("\nPhone:              ")
    phone = fake_in.indian_phone() if locale == "in" else fake_us.phone_number()
    tracker.add_pii(phone, "PHONE")

    tracker.add_text("\nEmail:              ")
    tracker.add_pii(fake.email(), "EMAIL")

    if locale == "in":
        tracker.add_text("\nPAN:                ")
        tracker.add_pii(fake_in.pan_number(), "PAN")
        tracker.add_text("\nAadhaar:            ")
        tracker.add_pii(fake_in.aadhaar_number(), "AADHAAR")
    else:
        tracker.add_text("\nSSN:                ")
        area = random.randint(100, 665)
        group = random.randint(1, 99)
        serial = random.randint(1, 9999)
        tracker.add_pii(f"{area:03d}-{group:02d}-{serial:04d}", "SSN")

    # Nominee
    tracker.add_text("""

--- NOMINEE DETAILS ---

Nominee Name:       """)
    tracker.add_pii(fake.name(), "PERSON_NAME")
    tracker.add_text("\nRelationship:       ")
    tracker.add_text(random.choice(["Spouse", "Son", "Daughter", "Father", "Mother"]))
    tracker.add_text("\nNominee DOB:        ")
    nom_dob = fake.date_of_birth(minimum_age=1, maximum_age=80)
    tracker.add_pii(nom_dob.strftime('%m/%d/%Y'), "DATE_OF_BIRTH")

    sum_assured = round(random.uniform(100000, 5000000), 2)

    tracker.add_text(f"""

--- POLICY DETAILS ---

Sum Assured:        ${sum_assured:>14,.2f}
Annual Premium:     ${premium:>14,.2f}
Policy Term:        {random.choice([10, 15, 20, 25, 30])} years
Premium Payment:    {'Annual' if random.random() > 0.5 else 'Monthly'}
Risk Commencement:  {fake.date_between('-365d', '-30d').strftime('%B %d, %Y')}
Maturity Date:      {fake.date_between('+3650d', '+10950d').strftime('%B %d, %Y')}

--- EXCLUSIONS ---

1. Death due to suicide within 12 months of policy commencement.
2. Death due to participation in hazardous activities not disclosed.
3. Pre-existing conditions not declared at the time of proposal.

For claims or queries, contact us at:
Customer Service: 1-800-555-0188
Email: claims@globalshieldinsurance.com

{'='*60}
""")

    return tracker.get_text(), tracker.get_ground_truth()


def generate_brokerage_statement(locale: str = "us") -> Tuple[str, List[Dict]]:
    """Generate a synthetic brokerage/investment statement."""
    tracker = PIITracker()
    fake = fake_us if locale == "us" else fake_in

    tracker.add_text(f"""{'='*60}
          {'EAGLE ROCK SECURITIES INC.' if locale == 'us' else 'TRIDENT CAPITAL SERVICES LTD.'}
            QUARTERLY INVESTMENT STATEMENT
             Q{random.randint(1,4)} - {datetime.now().year}
{'='*60}

--- INVESTOR INFORMATION ---

Name:                   """)
    tracker.add_pii(fake.name(), "PERSON_NAME")

    tracker.add_text("\nAccount Number:         ")
    tracker.add_pii(''.join(random.choices(string.digits, k=10)), "ACCOUNT_NUMBER")

    if locale == "in":
        tracker.add_text("\nPAN:                    ")
        tracker.add_pii(fake_in.pan_number(), "PAN")

        tracker.add_text("\nDemat Account:          ")
        tracker.add_pii(''.join(random.choices(string.digits, k=16)), "ACCOUNT_NUMBER")
    else:
        tracker.add_text("\nSSN:                    ")
        area = random.randint(100, 665)
        group = random.randint(1, 99)
        serial = random.randint(1, 9999)
        tracker.add_pii(f"{area:03d}-{group:02d}-{serial:04d}", "SSN")

    tracker.add_text("\nEmail:                  ")
    tracker.add_pii(fake.email(), "EMAIL")

    tracker.add_text("\nPhone:                  ")
    phone = fake_in.indian_phone() if locale == "in" else fake_us.phone_number()
    tracker.add_pii(phone, "PHONE")

    tracker.add_text("\nCorrespondence Address: ")
    tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

    # Portfolio
    stocks = [
        ("AAPL", "Apple Inc.", random.uniform(150, 200)),
        ("GOOGL", "Alphabet Inc.", random.uniform(130, 180)),
        ("MSFT", "Microsoft Corp.", random.uniform(350, 420)),
        ("AMZN", "Amazon.com Inc.", random.uniform(150, 190)),
        ("TSLA", "Tesla Inc.", random.uniform(200, 300)),
        ("NVDA", "NVIDIA Corp.", random.uniform(700, 900)),
        ("META", "Meta Platforms Inc.", random.uniform(400, 550)),
        ("JPM", "JPMorgan Chase & Co.", random.uniform(170, 210)),
    ]

    selected = random.sample(stocks, random.randint(3, 6))
    total_value = 0

    tracker.add_text(f"""

--- PORTFOLIO HOLDINGS ---

{'Symbol':<8} {'Company':<25} {'Qty':>6} {'Avg Cost':>12} {'Mkt Price':>12} {'Value':>14} {'P&L':>14}
{'-'*91}
""")

    for symbol, company, price in selected:
        qty = random.randint(5, 500)
        avg_cost = round(price * random.uniform(0.7, 1.1), 2)
        value = round(price * qty, 2)
        pnl = round((price - avg_cost) * qty, 2)
        total_value += value

        tracker.add_text(
            f"{symbol:<8} {company:<25} {qty:>6} ${avg_cost:>10,.2f} ${price:>10,.2f} ${value:>12,.2f} ${pnl:>12,.2f}\n"
        )

    tracker.add_text(f"""{'-'*91}
{'':>53} Total Portfolio Value: ${total_value:>12,.2f}

--- TRANSACTION HISTORY ---

{'Date':<14} {'Type':<8} {'Symbol':<8} {'Qty':>6} {'Price':>12} {'Amount':>14}
{'-'*62}
""")

    for _ in range(random.randint(4, 10)):
        tx_date = fake.date_between('-90d', 'today').strftime('%m/%d/%Y')
        tx_type = random.choice(["BUY", "SELL", "DIV"])
        symbol = random.choice(selected)[0]
        qty = random.randint(1, 100)
        price = round(random.uniform(50, 500), 2)
        amount = round(qty * price, 2)

        tracker.add_text(f"{tx_date:<14} {tx_type:<8} {symbol:<8} {qty:>6} ${price:>10,.2f} ${amount:>12,.2f}\n")

    tracker.add_text(f"""
--- DISCLAIMER ---
This statement is provided for informational purposes only.
Past performance is not indicative of future results.
All investments are subject to market risks.

{'='*60}
""")

    return tracker.get_text(), tracker.get_ground_truth()


def generate_credit_card_statement(locale: str = "us") -> Tuple[str, List[Dict]]:
    """Generate a synthetic credit card statement."""
    tracker = PIITracker()
    fake = fake_us if locale == "us" else fake_in

    tracker.add_text(f"""{'='*60}
              PREMIER CREDIT CARD STATEMENT
{'='*60}

--- CARDHOLDER INFORMATION ---

Cardholder Name:    """)
    tracker.add_pii(fake.name(), "PERSON_NAME")

    tracker.add_text("\nCard Number:        ")
    # Generate Luhn-valid credit card number
    card = fake.credit_card_number(card_type='visa')
    formatted_card = f"{card[:4]}-{card[4:8]}-{card[8:12]}-{card[12:]}"
    tracker.add_pii(formatted_card, "CREDIT_CARD")

    tracker.add_text("\nBilling Address:    ")
    tracker.add_pii(fake.address().replace('\n', ', '), "ADDRESS")

    tracker.add_text("\nPhone:              ")
    phone = fake_in.indian_phone() if locale == "in" else fake_us.phone_number()
    tracker.add_pii(phone, "PHONE")

    tracker.add_text("\nEmail:              ")
    tracker.add_pii(fake.email(), "EMAIL")

    prev_balance = round(random.uniform(500, 15000), 2)
    payments = round(random.uniform(200, prev_balance), 2)

    tracker.add_text(f"""

--- ACCOUNT SUMMARY ---

Statement Date:     {fake.date_between('-30d', 'today').strftime('%B %d, %Y')}
Payment Due Date:   {fake.date_between('+15d', '+30d').strftime('%B %d, %Y')}
Credit Limit:       ${round(random.uniform(5000, 50000), 2):>12,.2f}
Previous Balance:   ${prev_balance:>12,.2f}
Payments Received:  ${payments:>12,.2f}

--- TRANSACTIONS ---

{'Date':<14} {'Merchant':<35} {'Amount':>12}
{'-'*61}
""")

    total_charges = 0
    for _ in range(random.randint(6, 15)):
        tx_date = fake.date_between('-30d', 'today').strftime('%m/%d/%Y')
        merchant = fake.company()[:30]
        amount = round(random.uniform(5, 2000), 2)
        total_charges += amount
        tracker.add_text(f"{tx_date:<14} {merchant:<35} ${amount:>10,.2f}\n")

    new_balance = prev_balance - payments + total_charges
    min_payment = max(25, round(new_balance * 0.02, 2))

    tracker.add_text(f"""
{'-'*61}
Total Charges:      ${total_charges:>12,.2f}
New Balance:        ${new_balance:>12,.2f}
Minimum Payment:    ${min_payment:>12,.2f}

{'='*60}
""")

    return tracker.get_text(), tracker.get_ground_truth()


# ── Document Generator Registry ──

DOCUMENT_GENERATORS = {
    "bank_statement": generate_bank_statement,
    "tax_form": generate_tax_form,
    "loan_agreement": generate_loan_agreement,
    "insurance_letter": generate_insurance_letter,
    "brokerage_statement": generate_brokerage_statement,
    "credit_card_statement": generate_credit_card_statement,
}


def generate_all_documents(output_dir: str, ground_truth_dir: str,
                           count_per_type: int = 5) -> int:
    """
    Generate all document types and save with ground truth.

    Args:
        output_dir: Directory to save generated documents.
        ground_truth_dir: Directory to save ground truth JSON files.
        count_per_type: Number of documents to generate per type.

    Returns:
        Total number of documents generated.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(ground_truth_dir, exist_ok=True)

    total = 0
    locales = ["us", "in"]

    for doc_type, generator_fn in DOCUMENT_GENERATORS.items():
        for locale in locales:
            for i in range(count_per_type):
                # Reset random seed variation per document
                Faker.seed(42 + total * 137)
                random.seed(42 + total * 137)

                text, ground_truth = generator_fn(locale=locale)
                doc_name = f"{doc_type}_{locale}_{i+1:03d}"

                # Save document
                doc_path = os.path.join(output_dir, f"{doc_name}.txt")
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(text)

                # Save ground truth
                gt_path = os.path.join(ground_truth_dir, f"{doc_name}_gt.json")
                with open(gt_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "document": f"{doc_name}.txt",
                        "document_type": doc_type,
                        "locale": locale,
                        "total_pii_entities": len(ground_truth),
                        "entities": ground_truth
                    }, f, indent=2, ensure_ascii=False)

                total += 1

    return total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate synthetic financial documents with PII")
    parser.add_argument("--output", default="sample_data/input",
                        help="Output directory for documents")
    parser.add_argument("--ground-truth", default="sample_data/ground_truth",
                        help="Output directory for ground truth")
    parser.add_argument("--count", type=int, default=5,
                        help="Number of documents per type per locale")
    args = parser.parse_args()

    print(f"[INFO] Generating synthetic financial documents...")
    total = generate_all_documents(args.output, args.ground_truth, args.count)
    print(f"[OK] Generated {total} documents across {len(DOCUMENT_GENERATORS)} types")
    print(f"[DIR] Documents: {args.output}/")
    print(f"[DIR] Ground truth: {args.ground_truth}/")
