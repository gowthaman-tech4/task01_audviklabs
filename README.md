# PII Masking Pipeline for Unstructured Financial Data

This project is an advanced, multi-layered pipeline for detecting and masking Personally Identifiable Information (PII) from unstructured financial documents (bank statements, tax forms, W-2s, etc.).

## Features
- **Multi-layered extraction:** Uses Regex, Layout Analysis (`pdfplumber`), OCR (`pytesseract`), and NER.
- **Enterprise Privacy Decision Engine:** Implements a context-aware Risk Scoring Engine combined with a local LLM Verifier (via Ollama) to eliminate false positives (e.g. keeping "State Bank of India" but masking personal account holders).
- **Format-Preserving Masking:** Generates secure placeholder keys and maintains a mapping for complete data recovery.
- **Full-Stack Interface:** A React frontend (Vite) and FastAPI backend for uploading and viewing masked documents in real-time.

## Prerequisites
- Node.js (v18+)
- Python 3.10+
- Tesseract OCR installed on your system
- (Optional but Recommended) Ollama running locally with `llama3.2` for LLM verification.

## Setup Instructions

### 1. Backend Setup
1. Open a terminal and navigate to the project directory:
   ```bash
   cd audviklabs_task01
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   python api.py
   ```
   *The backend will run on `http://localhost:8000`.*

### 2. Frontend Setup
1. Open a **second** terminal window and navigate to the UI folder:
   ```bash
   cd audviklabs_task01/ui
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   *The frontend will be available at `http://localhost:5173`.*

## Running Evaluations
The evaluation suite has been updated to support batch processing and comprehensive reporting of Precision, Recall, and F1-Scores. 

To run the benchmarking suite and generate the performance report:
```bash
python evaluate.py --mode=verbose --output=report.json
```

Repository: https://github.com/gowthaman-tech4/audviklabs_task01
