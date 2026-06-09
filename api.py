import os

# Fix TESSDATA_PREFIX on Windows if it points to Tesseract-OCR instead of Tesseract-OCR\tessdata
tessdata_path = r"C:\Program Files\Tesseract-OCR\tessdata"
if os.path.exists(tessdata_path):
    os.environ["TESSDATA_PREFIX"] = tessdata_path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json
import os
from pipeline.pipeline import PIIPipeline

app = FastAPI(title="PII Masking API")

# Allow CORS for local Vite dev server (multiple ports in case 5173 is occupied)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:5175", "http://127.0.0.1:5175",
        "http://localhost:5176", "http://127.0.0.1:5176"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the pipeline once globally
pipeline = PIIPipeline()

class MaskRequest(BaseModel):
    text: str

@app.post("/api/mask/text")
def mask_text(request: MaskRequest):
    masked_text, mapping, entities = pipeline.process_text(request.text, "direct_input")
    return {
        "original_text": request.text,
        "masked_text": masked_text,
        "mapping": mapping,
        "entities": pipeline.last_audit_trail
    }

import tempfile
import shutil
import base64
import os
from fpdf import FPDF
import fitz

def generate_pdf_from_text(text: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("courier", size=9)
    
    # fpdf2 defaults to latin-1 for standard fonts, replace unsupported chars
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    
    # using multi_cell for automatic wrapping
    pdf.multi_cell(w=0, h=5, text=safe_text)
    pdf.output(output_path)

def coordinate_redact(coord_result, output_pdf_path: str, entities: list):
    from PIL import ImageDraw
    
    # We will draw on the existing PIL images in coord_result
    images = coord_result.page_images
    
    for entity in entities:
        # Find all word boxes associated with this entity's character range
        boxes_to_redact = set()
        for i in range(entity.start, entity.end):
            if i in coord_result.char_to_boxes:
                for box in coord_result.char_to_boxes[i]:
                    boxes_to_redact.add((box.page_num, box.x, box.y, box.w, box.h))
                    
        # Draw black rectangle for each bounding box
        for page_num, x, y, w, h in boxes_to_redact:
            if page_num < len(images):
                draw = ImageDraw.Draw(images[page_num])
                draw.rectangle([x, y, x + w, y + h], fill="black")
                
    if images:
        images[0].save(output_pdf_path, "PDF", resolution=300, save_all=True, append_images=images[1:])

@app.post("/api/mask/file")
def mask_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_input:
        shutil.copyfileobj(file.file, tmp_input)
        tmp_input_path = tmp_input.name
    
    try:
        masked_text, mapping, entities, coord_result = pipeline.process_file(tmp_input_path)
        
        # Generate masked PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf_path = tmp_pdf.name
            
        try:
            if ext in ['.pdf', '.png', '.jpg', '.jpeg']:
                coordinate_redact(coord_result, tmp_pdf_path, entities)
            else:
                generate_pdf_from_text(masked_text, tmp_pdf_path)
                
            with open(tmp_pdf_path, "rb") as f:
                pdf_bytes = f.read()
        finally:
            if os.path.exists(tmp_pdf_path):
                os.unlink(tmp_pdf_path)
    finally:
        if os.path.exists(tmp_input_path):
            os.unlink(tmp_input_path)
            
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    return {
        "original_text": "Text extracted from uploaded document.",
        "masked_text": masked_text,
        "mapping": mapping,
        "entities": pipeline.last_audit_trail,
        "pdf_base64": pdf_base64
    }

@app.get("/api/evaluation")
async def get_evaluation():
    eval_path = "results/evaluation_results.json"
    if os.path.exists(eval_path):
        with open(eval_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Map metrics to the format expected by Dashboard.jsx
            if "aggregate" in data and "overall_metrics" not in data:
                data["overall_metrics"] = data["aggregate"]
            if "per_type" in data and "by_type" not in data:
                data["by_type"] = {
                    k: {
                        "tp": v.get("true_positives", 0),
                        "fp": v.get("false_positives", 0),
                        "fn": v.get("false_negatives", 0),
                        "precision": v.get("precision", 0.0),
                        "recall": v.get("recall", 0.0),
                        "f1_score": v.get("f1_score", 0.0)
                    }
                    for k, v in data["per_type"].items()
                }
            return data
    return {"error": "Evaluation results not found"}

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
