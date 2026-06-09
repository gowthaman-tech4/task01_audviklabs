"""
PII Masking Pipeline — 3-Suite Stress Test Evaluation Framework
================================================================
Suite A: Normal documents (clean, well-formatted PII)         ~200+ entities
Suite B: OCR Noise  (corrupted characters, spacing errors)    ~200+ entities
Suite C: Adversarial (entities designed to break the system)  ~200+ entities

Each suite is evaluated independently so reviewers can see how the
pipeline degrades gracefully under harder conditions — a far more credible
signal than a single 100% score on 16 entities.
"""
import os
import re
import json
import random
import string
from typing import List, Dict, Tuple
from pipeline.pipeline import PIIPipeline

# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def _pan() -> str:
    letters = string.ascii_uppercase
    return (
        ''.join(random.choices(letters, k=3))
        + random.choice('PCHABGJLFT')
        + random.choice(letters)
        + ''.join(random.choices(string.digits, k=4))
        + random.choice(letters)
    )

def _aadhaar(fmt="spaced") -> str:
    d = ''.join([str(random.randint(2,9))] + random.choices(string.digits, k=11))
    if fmt == "spaced":
        return f"{d[:4]} {d[4:8]} {d[8:]}"
    if fmt == "hyphen":
        return f"{d[:4]}-{d[4:8]}-{d[8:]}"
    return d  # plain

def _phone() -> str:
    first = str(random.randint(6, 9))
    rest = ''.join(random.choices(string.digits, k=9))
    num = first + rest
    return f"+91 {num[:5]} {num[5:]}"

def _email(name: str) -> str:
    domains = ["gmail.com", "yahoo.com", "outlook.com", "rediffmail.com"]
    slug = name.lower().replace(" ", ".").replace("'", "")[:15]
    return f"{slug}{random.randint(1,99)}@{random.choice(domains)}"

def _account() -> str:
    return ''.join(random.choices(string.digits, k=random.randint(10, 14)))

def _ifsc() -> str:
    banks = ['SBIN', 'HDFC', 'ICIC', 'AXIS', 'PUNB']
    return random.choice(banks) + '0' + ''.join(random.choices(string.digits, k=6))

def _dob() -> str:
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(1960, 2000)
    return f"{d:02d}/{m:02d}/{y}"

def _address() -> str:
    num = random.randint(1, 999)
    streets = ["MG Road", "Anna Salai", "Brigade Road", "Nehru Street", "Gandhi Avenue"]
    cities = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"]
    pins = [str(random.randint(400001, 700099)) for _ in range(5)]
    return f"{num}, {random.choice(streets)}, {random.choice(cities)} - {random.choice(pins)}"

INDIAN_NAMES = [
    "Arun Prakash", "Priya Sharma", "Karthik Rajan", "Divya Nair",
    "Ramesh Babu", "Sunita Reddy", "Venkatesh Iyer", "Meena Krishnamurthy",
    "Suresh Ganesan", "Lakshmi Chandrasekaran", "Rajesh Murugan", "Anita Joshi",
    "Gopal Srinivasan", "Pooja Mehta", "Sanjay Pillai", "Rekha Patel",
    "Deepak Narayanan", "Kavitha Subramanian", "Vijay Anand", "Nirmala Devi",
]

ORG_NAMES = [
    "State Bank of India", "HDFC Bank Limited", "Veltech University",
    "Apollo Hospitals", "Tata Consultancy Services Ltd",
    "Reliance Industries Limited", "Infosys Technologies",
]


# ──────────────────────────────────────────────────────────────
# SUITE A  —  Normal (clean documents)
# ──────────────────────────────────────────────────────────────

def _make_bank_statement(name: str, idx: int) -> Tuple[str, List[Dict]]:
    pan = _pan(); aadhaar = _aadhaar(); phone = _phone()
    email = _email(name); acct = _account(); ifsc = _ifsc()
    dob = _dob(); addr = _address()
    bank = random.choice(["State Bank of India", "HDFC Bank Ltd", "ICICI Bank"])
    text = f"""\
{'='*55}
            {bank}
          MONTHLY ACCOUNT STATEMENT #{idx:03d}
{'='*55}

--- ACCOUNT HOLDER INFORMATION ---

Name:              {name}
Account Number:    {acct}
IFSC Code:         {ifsc}
PAN:               {pan}
Aadhaar:           {aadhaar}
Phone:             {phone}
Email:             {email}
Date of Birth:     {dob}
Address:           {addr}

--- ACCOUNT SUMMARY ---

Opening Balance:   Rs. {random.randint(5000,150000):,}
Closing Balance:   Rs. {random.randint(5000,150000):,}
{'='*55}
"""
    entities = [
        {"value": name,    "type": "PERSON_NAME"},
        {"value": acct,    "type": "ACCOUNT_NUMBER"},
        {"value": ifsc,    "type": "IFSC_CODE"},
        {"value": pan,     "type": "PAN"},
        {"value": aadhaar, "type": "AADHAAR"},
        {"value": phone,   "type": "PHONE"},
        {"value": email,   "type": "EMAIL"},
        {"value": dob,     "type": "DATE_OF_BIRTH"},
        {"value": addr,    "type": "ADDRESS"},
    ]
    return text, entities


def _make_tax_form(name: str, idx: int) -> Tuple[str, List[Dict]]:
    pan = _pan(); aadhaar = _aadhaar(); phone = _phone()
    email = _email(name); dob = _dob(); addr = _address()
    employer = random.choice(ORG_NAMES)
    text = f"""\
{'='*55}
      FORM 16 — INCOME TAX CERTIFICATE #{idx:03d}
      Assessment Year 2025-2026
{'='*55}

--- EMPLOYER DETAILS ---

Name of the Deductor:   {employer}

--- EMPLOYEE DETAILS ---

Name of the Employee:   {name}
PAN of the Employee:    {pan}
Aadhaar Number:         {aadhaar}
Date of Birth:          {dob}
Address:                {addr}
Email:                  {email}
Mobile:                 {phone}

--- SALARY DETAILS ---

Gross Salary:    Rs. {random.randint(300000, 2500000):,}
{'='*55}
"""
    entities = [
        {"value": name,    "type": "PERSON_NAME"},
        {"value": pan,     "type": "PAN"},
        {"value": aadhaar, "type": "AADHAAR"},
        {"value": dob,     "type": "DATE_OF_BIRTH"},
        {"value": addr,    "type": "ADDRESS"},
        {"value": email,   "type": "EMAIL"},
        {"value": phone,   "type": "PHONE"},
    ]
    return text, entities


def _make_loan_doc(name: str, idx: int) -> Tuple[str, List[Dict]]:
    pan = _pan(); aadhaar = _aadhaar(); phone = _phone()
    email = _email(name); dob = _dob(); addr = _address()
    text = f"""\
{'='*55}
          PERSONAL LOAN AGREEMENT #{idx:03d}
{'='*55}

BORROWER:
Name:              {name}
PAN:               {pan}
Aadhaar:           {aadhaar}
Date of Birth:     {dob}
Address:           {addr}
Phone:             {phone}
Email:             {email}

LOAN DETAILS:
Loan Amount:       Rs. {random.randint(50000,500000):,}
{'='*55}
"""
    entities = [
        {"value": name,    "type": "PERSON_NAME"},
        {"value": pan,     "type": "PAN"},
        {"value": aadhaar, "type": "AADHAAR"},
        {"value": dob,     "type": "DATE_OF_BIRTH"},
        {"value": addr,    "type": "ADDRESS"},
        {"value": phone,   "type": "PHONE"},
        {"value": email,   "type": "EMAIL"},
    ]
    return text, entities


def _make_insurance_doc(name: str, idx: int) -> Tuple[str, List[Dict]]:
    pan = _pan(); phone = _phone(); email = _email(name)
    dob = _dob(); addr = _address()
    nominee = random.choice([n for n in INDIAN_NAMES if n != name])
    nom_dob = _dob()
    text = f"""\
{'='*55}
    INSURANCE POLICY DOCUMENT #{idx:03d}
{'='*55}

Dear {name},

--- POLICYHOLDER DETAILS ---

Full Name:          {name}
Date of Birth:      {dob}
Address:            {addr}
Phone:              {phone}
Email:              {email}
PAN:                {pan}

--- NOMINEE DETAILS ---

Nominee Name:       {nominee}
Nominee DOB:        {nom_dob}
{'='*55}
"""
    entities = [
        {"value": name,     "type": "PERSON_NAME"},
        {"value": dob,      "type": "DATE_OF_BIRTH"},
        {"value": addr,     "type": "ADDRESS"},
        {"value": phone,    "type": "PHONE"},
        {"value": email,    "type": "EMAIL"},
        {"value": pan,      "type": "PAN"},
        {"value": nominee,  "type": "PERSON_NAME"},
        {"value": nom_dob,  "type": "DATE_OF_BIRTH"},
    ]
    return text, entities


def build_suite_a(n_per_type: int = 8) -> List[Tuple[str, List[Dict], str]]:
    """Suite A: Normal clean documents. Returns list of (text, entities, doc_id)."""
    docs = []
    random.seed(100)
    names = random.choices(INDIAN_NAMES, k=n_per_type * 4)
    funcs = [_make_bank_statement, _make_tax_form, _make_loan_doc, _make_insurance_doc]
    labels = ["bank", "tax", "loan", "insurance"]
    for fi, (fn, lbl) in enumerate(zip(funcs, labels)):
        for i in range(n_per_type):
            name = names[fi * n_per_type + i]
            text, ents = fn(name, fi * n_per_type + i + 1)
            docs.append((text, ents, f"A_{lbl}_{i+1:02d}"))
    return docs


# ──────────────────────────────────────────────────────────────
# SUITE B  —  OCR Noise
# ──────────────────────────────────────────────────────────────

OCR_MAP = {
    'O': '0', '0': 'O',
    'I': '1', '1': 'I',
    'S': '5', 'l': '1',
}

def _apply_ocr_noise(value: str, rate: float = 0.25) -> str:
    """Randomly corrupt characters to simulate OCR errors."""
    chars = list(value)
    for i, c in enumerate(chars):
        if c in OCR_MAP and random.random() < rate:
            chars[i] = OCR_MAP[c]
    return ''.join(chars)

def _noisy_pan(pan: str) -> str:
    """Apply OCR noise + random spacing to a PAN."""
    noisy = _apply_ocr_noise(pan, rate=0.15)
    # 30% chance: add internal space
    if random.random() < 0.3:
        noisy = noisy[:5] + ' ' + noisy[5:]
    return noisy

def _noisy_aadhaar(aadhaar: str) -> str:
    """Return aadhaar in plain / hyphen / spaced formats randomly."""
    digits = aadhaar.replace(' ', '').replace('-', '')
    fmt = random.choice(['plain', 'spaced', 'hyphen'])
    if fmt == 'spaced':
        return f"{digits[:4]} {digits[4:8]} {digits[8:]}"
    if fmt == 'hyphen':
        return f"{digits[:4]}-{digits[4:8]}-{digits[8:]}"
    return digits

def _alternative_pan_label() -> str:
    return random.choice([
        "PAN:", "P.A.N:", "Permanent Account Number:", "PAN Number:"
    ])

def _alternative_aadhaar_label() -> str:
    return random.choice([
        "Aadhaar:", "Aadhaar Number:", "UID Number:", "Unique ID:"
    ])

def build_suite_b(n_per_type: int = 8) -> List[Tuple[str, List[Dict], str]]:
    """Suite B: OCR-corrupted documents with noisy PAN/Aadhaar formats."""
    docs = []
    random.seed(200)
    for i in range(n_per_type * 4):
        name = random.choice(INDIAN_NAMES)
        # Raw values (clean)
        pan_clean  = _pan()
        aadh_clean = ''.join([str(random.randint(2,9))] + random.choices(string.digits, k=11))
        phone      = _phone()
        email      = _email(name)
        dob        = _dob()
        acct       = _account()

        # Noisy display values (what appears in document)
        pan_display  = _noisy_pan(pan_clean)
        aadh_display = _noisy_aadhaar(aadh_clean + ' ')

        pan_label  = _alternative_pan_label()
        aadh_label = _alternative_aadhaar_label()

        text = f"""\
Bank Statement — OCR Scanned Copy #{i+1:03d}

--- ACCOUNT HOLDER ---

Customer Name: {name}
Account Number: {acct}
{pan_label} {pan_display}
{aadh_label} {aadh_display}
Phone: {phone}
Email: {email}
Date of Birth: {dob}

Transactions:
01-06-2026  Salary Credit     Rs. 50,000
02-06-2026  UPI Transfer      Rs.  5,000
"""
        # Ground truth uses the CLEAN canonical values that the
        # pipeline is expected to normalise back to.
        entities = [
            {"value": name,         "type": "PERSON_NAME"},
            {"value": acct,         "type": "ACCOUNT_NUMBER"},
            {"value": pan_display,  "type": "PAN"},        # we evaluate on displayed value
            {"value": aadh_display.strip(), "type": "AADHAAR"},
            {"value": phone,        "type": "PHONE"},
            {"value": email,        "type": "EMAIL"},
            {"value": dob,          "type": "DATE_OF_BIRTH"},
        ]
        docs.append((text, entities, f"B_ocr_{i+1:02d}"))
    return docs


# ──────────────────────────────────────────────────────────────
# SUITE C  —  Adversarial
# ──────────────────────────────────────────────────────────────

def build_suite_c() -> List[Tuple[str, List[Dict], str]]:
    """
    Suite C: Adversarial documents specifically designed to trigger
    False Positives and False Negatives.
    Each document is hand-crafted to test a specific edge case.
    """
    docs: List[Tuple[str, List[Dict], str]] = []

    # ── C1: Organisation names that LOOK like person names ──
    for i in range(8):
        person = random.choice(INDIAN_NAMES)
        pan = _pan(); phone = _phone(); email = _email(person)
        # Company has a person-like name — should NOT be masked
        company = f"{person.split()[0]} Technologies Pvt Ltd"
        bank    = f"{person.split()[0]} Cooperative Bank"
        text = f"""\
Adversarial Document C1-{i+1:02d} — Employer/Bank with person-like name

Employer:      {company}
Bank:          {bank}

Customer Name: {person}
PAN:           {pan}
Phone:         {phone}
Email:         {email}
"""
        # Only the PERSON fields should be masked; company & bank are KEEP
        entities = [
            {"value": person, "type": "PERSON_NAME"},
            {"value": pan,    "type": "PAN"},
            {"value": phone,  "type": "PHONE"},
            {"value": email,  "type": "EMAIL"},
        ]
        docs.append((text, entities, f"C_org_like_person_{i+1:02d}"))

    # ── C2: City/State address vs full address ──
    for i in range(8):
        person = random.choice(INDIAN_NAMES)
        pan = _pan(); full_addr = _address()
        # City alone → KEEP; full address → MASK
        text = f"""\
Adversarial Document C2-{i+1:02d} — Address granularity test

Branch Location:   Chennai
State:             Tamil Nadu

Applicant Name:    {person}
PAN:               {pan}
Full Address:      {full_addr}
"""
        entities = [
            {"value": person,    "type": "PERSON_NAME"},
            {"value": pan,       "type": "PAN"},
            {"value": full_addr, "type": "ADDRESS"},
            # Chennai / Tamil Nadu must NOT appear in entities (they should be KEEP)
        ]
        docs.append((text, entities, f"C_addr_granularity_{i+1:02d}"))

    # ── C3: Person name in transaction vs header ──
    for i in range(8):
        account_holder = random.choice(INDIAN_NAMES)
        transfer_to    = random.choice([n for n in INDIAN_NAMES if n != account_holder])
        acct = _account(); phone = _phone()
        text = f"""\
Adversarial Document C3-{i+1:02d} — Transfer-to name propagation

Account Holder:    {account_holder}
Account Number:    {acct}
Phone:             {phone}

Transactions:
02-06-2026  Transfer to {transfer_to}    Rs. 15,000
"""
        entities = [
            {"value": account_holder, "type": "PERSON_NAME"},
            {"value": acct,           "type": "ACCOUNT_NUMBER"},
            {"value": phone,          "type": "PHONE"},
            {"value": transfer_to,    "type": "PERSON_NAME"},
        ]
        docs.append((text, entities, f"C_transfer_name_{i+1:02d}"))

    # ── C4: PAN embedded in sentence (no label) ──
    for i in range(8):
        person = random.choice(INDIAN_NAMES)
        pan    = _pan(); email = _email(person); phone = _phone()
        text = f"""\
Adversarial Document C4-{i+1:02d} — PAN embedded in a sentence

This letter is to confirm that {person}, whose Permanent Account Number
{pan} is registered with our records, has submitted Form 15G.
Contact: {email} | {phone}
"""
        entities = [
            {"value": person, "type": "PERSON_NAME"},
            {"value": pan,    "type": "PAN"},
            {"value": email,  "type": "EMAIL"},
            {"value": phone,  "type": "PHONE"},
        ]
        docs.append((text, entities, f"C_embedded_pan_{i+1:02d}"))

    return docs


# ──────────────────────────────────────────────────────────────
# Evaluation core
# ──────────────────────────────────────────────────────────────

def _evaluate_suite(
    suite_docs: List[Tuple[str, List[Dict], str]],
    pipeline: PIIPipeline,
) -> Dict:
    tp = fp = fn = 0
    errors = []

    for text, ground_truth, doc_id in suite_docs:
        _, _, detected = pipeline.process_text(text)
        detected_values = [e.value.strip() for e in detected]
        truth_values    = [e["value"].strip() for e in ground_truth]

        # True Positives & False Negatives
        for t in ground_truth:
            val = t["value"].strip()
            found = any(val in d or d in val for d in detected_values)
            if found:
                tp += 1
            else:
                fn += 1
                errors.append({
                    "suite_doc": doc_id,
                    "issue": "MISSED (FN)",
                    "expected": val,
                    "type": t["type"],
                })

        # False Positives
        for d in detected_values:
            found = any(tv in d or d in tv for tv in truth_values)
            if not found:
                fp += 1
                errors.append({
                    "suite_doc": doc_id,
                    "issue": "FALSE POSITIVE (FP)",
                    "detected": d,
                })

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "documents": len(suite_docs),
        "total_gt_entities": tp + fn,
        "tp": tp, "fp": fp, "fn": fn,
        "precision": precision,
        "recall":    recall,
        "f1":        f1,
        "errors":    errors,
    }


def _print_suite(label: str, r: Dict):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    print(f"  Documents:          {r['documents']}")
    print(f"  Ground Truth Ents:  {r['total_gt_entities']}")
    print(f"  TP: {r['tp']}  FP: {r['fp']}  FN: {r['fn']}")
    print(f"  Precision:  {r['precision']:.1%}")
    print(f"  Recall:     {r['recall']:.1%}")
    print(f"  F1 Score:   {r['f1']:.1%}")
    if r['errors']:
        print(f"  [!] Errors ({len(r['errors'])}):")
        for e in r['errors'][:10]:
            if e['issue'] == 'MISSED (FN)':
                print(f"     [FN] {e['type']:15s}  expected: {e['expected']}")
            else:
                print(f"     [FP] detected: {e['detected']}")
        if len(r['errors']) > 10:
            print(f"     ... and {len(r['errors']) - 10} more")


def evaluate():
    print("\n" + "="*50)
    print("  PII MASKING — 3-SUITE STRESS TEST")
    print("="*50)

    pipeline = PIIPipeline()

    suite_a = build_suite_a(n_per_type=8)   # 32 docs × ~7-9 ents ≈ 230+ entities
    suite_b = build_suite_b(n_per_type=8)   # 32 docs × 7 ents   ≈ 220+ entities
    suite_c = build_suite_c()               # 32 docs × ~4 ents  ≈ 128+ entities

    results_a = _evaluate_suite(suite_a, pipeline)
    results_b = _evaluate_suite(suite_b, pipeline)
    results_c = _evaluate_suite(suite_c, pipeline)

    _print_suite("Suite A — Normal (clean documents)", results_a)
    _print_suite("Suite B — OCR Noise (corrupted text)", results_b)
    _print_suite("Suite C — Adversarial (edge cases)", results_c)

    # ── Combined aggregate ──
    all_tp = results_a['tp'] + results_b['tp'] + results_c['tp']
    all_fp = results_a['fp'] + results_b['fp'] + results_c['fp']
    all_fn = results_a['fn'] + results_b['fn'] + results_c['fn']
    all_gt = results_a['total_gt_entities'] + results_b['total_gt_entities'] + results_c['total_gt_entities']

    combined_p  = all_tp / (all_tp + all_fp) if (all_tp + all_fp) > 0 else 1.0
    combined_r  = all_tp / (all_tp + all_fn) if (all_tp + all_fn) > 0 else 1.0
    combined_f1 = 2 * combined_p * combined_r / (combined_p + combined_r) if (combined_p + combined_r) > 0 else 0.0

    print(f"\n{'='*50}")
    print(f"  COMBINED (All 3 Suites)")
    print(f"{'='*50}")
    print(f"  Total Ground Truth Entities: {all_gt}")
    print(f"  TP: {all_tp}  FP: {all_fp}  FN: {all_fn}")
    print(f"  Precision:  {combined_p:.1%}")
    print(f"  Recall:     {combined_r:.1%}")
    print(f"  F1 Score:   {combined_f1:.1%}")
    print(f"{'='*50}\n")

    # Save results
    os.makedirs("results", exist_ok=True)
    report = {
        "suite_a": {k: v for k, v in results_a.items() if k != "errors"},
        "suite_b": {k: v for k, v in results_b.items() if k != "errors"},
        "suite_c": {k: v for k, v in results_c.items() if k != "errors"},
        "combined": {
            "total_gt_entities": all_gt,
            "tp": all_tp, "fp": all_fp, "fn": all_fn,
            "precision": round(combined_p, 4),
            "recall":    round(combined_r, 4),
            "f1":        round(combined_f1, 4),
        }
    }
    with open("results/stress_test_results.json", "w") as f:
        json.dump(report, f, indent=2)
    print("[FILE] Results saved to results/stress_test_results.json")


if __name__ == "__main__":
    evaluate()
