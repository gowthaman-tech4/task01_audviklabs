"""
Main entry point — runs the full PII masking pipeline:
1. Generate synthetic data (if needed)
2. Run pipeline on all documents
3. Evaluate accuracy
4. Generate report
"""
import os
import sys
import json
import argparse
import time

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_generate(args):
    """Generate synthetic documents."""
    from data_generator.generator import generate_all_documents

    print("\n" + "="*60)
    print("  STEP 1: GENERATING SYNTHETIC FINANCIAL DOCUMENTS")
    print("="*60 + "\n")

    total = generate_all_documents(
        output_dir=args.input_dir,
        ground_truth_dir=args.gt_dir,
        count_per_type=args.count
    )
    print(f"\n[OK] Generated {total} documents")
    return total


def run_pipeline(args):
    """Run PII masking pipeline on all documents."""
    from pipeline.pipeline import PIIPipeline

    print("\n" + "="*60)
    print("  STEP 2: RUNNING PII MASKING PIPELINE")
    print("="*60 + "\n")

    pipeline = PIIPipeline(
        spacy_model=args.spacy_model,
        use_ner=not args.no_ner,
        confidence_threshold=args.confidence
    )

    start_time = time.time()
    results = pipeline.process_directory(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        mapping_dir=args.mapping_dir
    )
    elapsed = time.time() - start_time

    print(f"\n[OK] Processed {results['processed']}/{results['total_files']} files")
    print(f"   Total entities masked: {results['total_entities']}")
    print(f"   Time elapsed: {elapsed:.1f}s")

    if results['failed'] > 0:
        print(f"   [WARN] Failed: {results['failed']} files")

    return results


def run_evaluate(args):
    """Evaluate masking accuracy."""
    from evaluation.evaluator import PIIEvaluator, generate_report

    print("\n" + "="*60)
    print("  STEP 3: EVALUATING ACCURACY")
    print("="*60 + "\n")

    evaluator = PIIEvaluator(iou_threshold=args.iou)
    results = evaluator.evaluate_batch(args.mapping_dir, args.gt_dir)

    # Print summary
    agg = results.get("aggregate", {})
    print(f"  Results:")
    print(f"     Precision:  {agg.get('precision', 0):.2%}")
    print(f"     Recall:     {agg.get('recall', 0):.2%}")
    print(f"     F1 Score:   {agg.get('f1_score', 0):.2%}")
    print(f"     Accuracy:   {agg.get('accuracy', 0):.2%}")
    print(f"     TP: {agg.get('true_positives', 0)} | "
          f"FP: {agg.get('false_positives', 0)} | "
          f"FN: {agg.get('false_negatives', 0)}")

    # Check if target accuracy met
    accuracy = agg.get('accuracy', 0)
    if accuracy >= 0.95:
        print(f"\n  >>> TARGET MET: {accuracy:.2%} >= 95%")
    else:
        print(f"\n  >>> TARGET NOT MET: {accuracy:.2%} < 95%")

    # Generate report
    report_path = os.path.join(args.results_dir, "evaluation_report.md")
    report = generate_report(results, report_path)
    print(f"\n  Report: {report_path}")

    # Save raw JSON
    json_path = os.path.join(args.results_dir, "evaluation_results.json")
    os.makedirs(args.results_dir, exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"  Raw data: {json_path}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="PII Masking Pipeline for Unstructured Financial Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline (generate + mask + evaluate)
  python main.py --all

  # Generate documents only
  python main.py --generate --count 10

  # Run masking only (on existing documents)
  python main.py --mask

  # Evaluate only (on existing masked outputs)
  python main.py --evaluate

  # Run without NER (regex only, faster)
  python main.py --all --no-ner
        """
    )

    # Actions
    parser.add_argument("--all", action="store_true",
                        help="Run full pipeline: generate -> mask -> evaluate")
    parser.add_argument("--generate", action="store_true",
                        help="Generate synthetic documents")
    parser.add_argument("--mask", action="store_true",
                        help="Run masking pipeline")
    parser.add_argument("--evaluate", action="store_true",
                        help="Evaluate accuracy")

    # Paths
    parser.add_argument("--input-dir", default="sample_data/input",
                        help="Input documents directory")
    parser.add_argument("--output-dir", default="sample_data/masked_output",
                        help="Masked output directory")
    parser.add_argument("--mapping-dir", default="sample_data/mappings",
                        help="Mapping files directory")
    parser.add_argument("--gt-dir", default="sample_data/ground_truth",
                        help="Ground truth directory")
    parser.add_argument("--results-dir", default="results",
                        help="Results directory")

    # Pipeline options
    parser.add_argument("--count", type=int, default=5,
                        help="Documents per type per locale (default: 5)")
    parser.add_argument("--spacy-model", default="en_core_web_sm",
                        help="spaCy model to use (default: en_core_web_sm)")
    parser.add_argument("--no-ner", action="store_true",
                        help="Disable NER (regex only mode)")
    parser.add_argument("--confidence", type=float, default=0.5,
                        help="Minimum confidence threshold (default: 0.5)")
    parser.add_argument("--iou", type=float, default=0.5,
                        help="IoU threshold for evaluation (default: 0.5)")

    args = parser.parse_args()

    # Default: run all if no action specified
    if not (args.all or args.generate or args.mask or args.evaluate):
        args.all = True

    print("\n" + "=" * 60)
    print("  PII MASKING PIPELINE FOR FINANCIAL DOCUMENTS")
    print("=" * 60)

    start_total = time.time()

    if args.all or args.generate:
        run_generate(args)

    if args.all or args.mask:
        run_pipeline(args)

    if args.all or args.evaluate:
        run_evaluate(args)

    elapsed_total = time.time() - start_total
    print(f"\n{'='*60}")
    print(f"  Total time: {elapsed_total:.1f}s")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
