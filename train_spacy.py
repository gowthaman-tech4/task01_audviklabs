"""
spaCy NER Fine-Tuning Harness.

Converts generated synthetic documents and ground truth labels into
spaCy's binary training format (.spacy) and sets up the config for NER training.
"""
import os
import json
import random
import argparse
import subprocess
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

def load_dataset(input_dir: str, gt_dir: str) -> list:
    """Load text and entities from the generated dataset directories."""
    data = []
    
    # List all ground truth JSON files
    gt_files = [f for f in os.listdir(gt_dir) if f.endswith("_gt.json")]
    print(f"[INFO] Found {len(gt_files)} ground truth label files.")
    
    for gt_file in tqdm(gt_files, desc="Loading dataset"):
        base_name = gt_file.replace("_gt.json", "")
        txt_path = os.path.join(input_dir, f"{base_name}.txt")
        gt_path = os.path.join(gt_dir, gt_file)
        
        if not os.path.exists(txt_path):
            continue
            
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        with open(gt_path, 'r', encoding='utf-8') as f:
            gt_data = json.load(f)
            
        entities = []
        for ent in gt_data.get("entities", []):
            entities.append((ent["start"], ent["end"], ent["type"]))
            
        data.append((text, {"entities": entities}))
        
    return data

def convert_to_spacy_format(data: list, nlp, output_path: str):
    """Convert dataset into spaCy's DocBin and save to disk."""
    db = DocBin()
    skipped_count = 0
    total_ents = 0
    
    for text, annotations in data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annotations["entities"]:
            # Standardizing character spans onto spaCy token boundaries
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                # Try expanding span slightly if contract fails
                span = doc.char_span(start, end, label=label, alignment_mode="expand")
                
            if span is None:
                skipped_count += 1
                continue
                
            ents.append(span)
            total_ents += 1
            
        # Deduplicate overlapping spans to avoid spaCy validation errors
        filtered_ents = spacy.util.filter_spans(ents)
        doc.ents = filtered_ents
        db.add(doc)
        
    db.to_disk(output_path)
    print(f"[OK] Saved {len(data)} documents to {output_path}")
    print(f"     Total entities: {total_ents} | Misaligned spans skipped: {skipped_count}")

def setup_training(args):
    """Prepares the training configuration and generates the training data files."""
    print(f"\n[STEP 1] Loading and splitting dataset...")
    raw_data = load_dataset(args.input_dir, args.gt_dir)
    
    # Set seed for reproducibility and shuffle
    random.seed(42)
    random.shuffle(raw_data)
    
    # 80/20 train/dev split
    split_idx = int(len(raw_data) * 0.8)
    train_data = raw_data[:split_idx]
    dev_data = raw_data[split_idx:]
    
    print(f"[INFO] Dataset split: {len(train_data)} train documents | {len(dev_data)} validation documents")
    
    # Initialize spaCy blank model
    nlp = spacy.blank("en")
    
    # Save training sets
    os.makedirs(args.data_dir, exist_ok=True)
    train_spacy_path = os.path.join(args.data_dir, "train.spacy")
    dev_spacy_path = os.path.join(args.data_dir, "dev.spacy")
    
    print(f"\n[STEP 2] Converting training set...")
    convert_to_spacy_format(train_data, nlp, train_spacy_path)
    
    print(f"\n[STEP 3] Converting validation set...")
    convert_to_spacy_format(dev_data, nlp, dev_spacy_path)
    
    # Generate base training config file
    config_path = os.path.join(args.data_dir, "config.cfg")
    print(f"\n[STEP 4] Initializing spaCy training config: {config_path}")
    cmd = [
        "python", "-m", "spacy", "init", "config", config_path,
        "--lang", "en",
        "--pipeline", "ner",
        "--optimize", "accuracy",
        "--force"
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"[OK] spaCy configuration initialized successfully!")
    except Exception as e:
        print(f"[FAIL] Error generating config: {e}")
        print("[TIP] You can generate it manually by running:")
        print(f"      {' '.join(cmd)}")
        
    print(f"\n{'='*60}")
    print("  SPACY TRAINING PREPARATION COMPLETE!")
    print(f"{'='*60}")
    print(f"1. Train Set:      {train_spacy_path}")
    print(f"2. Validation Set:  {dev_spacy_path}")
    print(f"3. Config File:     {config_path}")
    print("\nTo launch NER training, execute the following command:")
    print(f"python -m spacy train {config_path} --output ./model_output --paths.train {train_spacy_path} --paths.dev {dev_spacy_path}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="spaCy fine-tuning data prep and config builder")
    parser.add_argument("--input-dir", default="sample_data/input", help="Directory containing text documents")
    parser.add_argument("--gt-dir", default="sample_data/ground_truth", help="Directory containing JSON labels")
    parser.add_argument("--data-dir", default="evaluation/spacy_train", help="Directory to save config and .spacy outputs")
    args = parser.parse_args()
    
    setup_training(args)
