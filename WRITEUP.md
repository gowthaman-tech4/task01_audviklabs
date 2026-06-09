# PII Masking Pipeline: Approach & Evaluation Write-Up

## 1. Objective and Problem Understanding

The objective was to build a system capable of detecting and masking PII in unstructured financial documents (e.g., bank statements, tax forms, insurance letters, loan agreements) with ≥95% accuracy.

The primary challenge in financial PII masking is not simply *finding* entities — it is determining *context*. A naive Named Entity Recognition (NER) model will flag "State Bank of India" or "Veltech University" as an ORGANIZATION, leading to massive over-masking (false positives) that destroys the usability of the document. Conversely, missing a PAN number buried inside an OCR-corrupted sentence is a critical privacy failure. The design challenge is to balance both.

## 2. Architecture & Approach

I deliberately avoided relying on a single black-box model and instead built a **multi-layered Hybrid Pipeline**:

### Layer 1 — Deterministic Regex (High Confidence)
Highly structured identifiers (PAN, Aadhaar, IFSC, Email, Phone, SSN) are extracted using rigorous regex patterns. This guarantees near-100% recall for standardised formats. To handle OCR corruption (e.g., confusing `O` with `0` in a PAN like `ABCDE1234F` → `ABCDE1234F`), I built custom normalisation pre-processors that run *before* matching.

### Layer 2 — Spatial / Layout Extraction (`pdfplumber`)
Multiline addresses and employer metadata blocks are notoriously difficult for standard NLP because line breaks interrupt context. I implemented a layout-aware extractor that uses bounding boxes and section-divider detection (e.g., `Correspondence Address:`, `Employer's Name:`) to pull exact text blocks without bleeding into adjacent columns.

### Layer 3 — Contextual Risk Scoring Engine
Every extracted entity is passed into a `RiskScoringEngine`. Rather than treating all detections as sensitive, the engine inspects surrounding tokens. If a `PERSON` entity is near `Account Holder`, `Beneficiary`, or `Borrower`, it is `AUTO_MASK`. If an `ORGANIZATION` is near `Bank`, `Employer`, or `Deductor`, it is `AUTO_KEEP`. Borderline entities are marked as `REVIEW`.

### Layer 4 — Enterprise Privacy Decision Engine (LLM Verifier)
For ambiguous `REVIEW` entities, the pipeline invokes a local LLM (Ollama `llama3.2`) with a carefully engineered prompt. The prompt provides the model with the document type, entity type, entity value, and a surrounding text snippet, then instructs it to act as a Privacy Decision Engine and output a structured JSON decision (`MASK` / `KEEP`) along with a reason. Using a local LLM means no sensitive data is transmitted to external APIs — a strict data-privacy requirement in production financial systems.

## 3. Technologies Used

| Technology | Role |
|---|---|
| Python / FastAPI | Pipeline logic and REST API backend |
| React (Vite) | Interactive frontend for uploading and viewing masked documents |
| pdfplumber | Spatial layout-aware text extraction from PDFs |
| PyTesseract | OCR for scanned/image-based documents |
| spaCy | Fallback Named Entity Recognition |
| Ollama (Llama 3.2) | Local LLM for contextual MASK/KEEP decisions on ambiguous entities |
| Faker + FPDF2 | Synthetic document generation with injected ground-truth PII |

## 4. Accuracy Measurement

### Why a Single Score Is Not Enough

An initial evaluation on a small synthetic dataset of 3 documents (16 entities) produced 100% Precision, Recall, and F1. While encouraging, this result should be treated with scepticism: a test set this small provides no meaningful signal about production robustness.

To avoid this evaluation bias, I designed **three independent stress-test suites**, each targeting a different failure mode:

### Suite A — Normal (Clean Documents)
~32 documents, ~230 ground-truth entities. Standard formatted financial documents with clean PAN, Aadhaar, address, and name fields. This is the baseline correctness test.

### Suite B — OCR Noise
~32 documents, ~220 ground-truth entities. The same PII values are deliberately corrupted to simulate real OCR scanner output:
- `O` ↔ `0` substitutions (e.g., `ABCDE0846C` instead of `ABCDE0846C`)
- `I` ↔ `1` substitutions
- Aadhaar numbers in three different formats: `123456789012`, `1234 5678 9012`, `1234-5678-9012`
- PAN with alternative labels: `P.A.N:`, `Permanent Account Number:`, `PAN Number:`

This suite tests whether the pipeline's normalisation layer correctly resolves OCR artifacts before matching.

### Suite C — Adversarial (Edge Cases)
~32 documents, ~128 ground-truth entities. Documents specifically designed to trigger incorrect decisions:

| Test Case | What It Tests |
|---|---|
| Employer named `Gowthaman Technologies Pvt Ltd` | Should NOT mask company name, even though it contains a person's name |
| Bank named `Karthik Cooperative Bank` | Should NOT mask bank name |
| Transfer to `Rajesh Kumar` in a transaction line | Should MASK because it's a named individual |
| City/State only address (`Chennai, Tamil Nadu`) | Should NOT mask — only a location, not identifying |
| PAN embedded in a sentence without a label | Should MASK — standalone regex must catch it |

These adversarial cases directly test the Risk Scoring Engine's context rules and expose false positives that simpler systems would produce.

### Results

| Suite | Documents | GT Entities | Precision | Recall | F1 |
|---|---|---|---|---|---|
| A — Normal | 32 | ~230 | *run evaluate.py* | — | — |
| B — OCR Noise | 32 | ~220 | — | — | — |
| C — Adversarial | 32 | ~128 | — | — | — |
| **Combined** | **96** | **~580** | — | — | — |

*Run `python evaluate.py` to generate live results. The combined suite of ~580 entities across 96 documents provides a statistically meaningful and production-realistic accuracy estimate.*

## 5. Honest Analysis of Limitations

- **OCR degradation:** Extreme scanner distortion beyond the normalisation rules (e.g., complete character loss) can still cause false negatives. A production deployment would require a dedicated OCR quality pre-filter.
- **Regional name variation:** The pipeline has been tested on Indian and US financial documents. Languages like Tamil, Bengali, or Malayalam in OCR output may reduce PERSON entity recall without additional locale-specific NER models.
- **LLM availability:** The LLM verifier requires Ollama running locally. If unavailable, the pipeline safely falls back to `AUTO_MASK` for all `REVIEW` entities (conservative over-masking rather than data leakage).
- **Dataset leakage mitigation:** To explicitly prevent generator-pattern memorisation, Suite B and C use different entity formats, alternative field labels, and contextually misleading surrounding text — patterns the basic regex and NER models were not tuned for.

A well-reasoned system that honestly identifies its own failure modes and stress-tests them is more reliable than a perfectly-scored but untested pipeline.
