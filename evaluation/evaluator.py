"""
PII Masking Evaluation Framework.

Compares pipeline detections against ground truth labels to compute
precision, recall, F1 score, and overall accuracy.
"""
import os
import json
import glob
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class PIIEvaluator:
    """
    Evaluates PII detection accuracy against ground truth.

    A detection is considered correct if:
    1. It overlaps with a ground truth entity by ≥80% (IoU).
    2. The PII type matches.
    """

    def __init__(self, iou_threshold: float = 0.5):
        """
        Args:
            iou_threshold: Minimum Intersection-over-Union ratio to count
                          a detection as a true positive (0.0 to 1.0).
        """
        self.iou_threshold = iou_threshold

    def _compute_iou(self, pred_start: int, pred_end: int,
                     gt_start: int, gt_end: int) -> float:
        """Compute Intersection over Union between two spans."""
        intersection_start = max(pred_start, gt_start)
        intersection_end = min(pred_end, gt_end)

        if intersection_start >= intersection_end:
            return 0.0

        intersection = intersection_end - intersection_start
        union = (pred_end - pred_start) + (gt_end - gt_start) - intersection

        return intersection / union if union > 0 else 0.0

    def _compute_overlap_ratio(self, pred_start: int, pred_end: int,
                                gt_start: int, gt_end: int) -> float:
        """Compute how much of ground truth is covered by prediction."""
        intersection_start = max(pred_start, gt_start)
        intersection_end = min(pred_end, gt_end)

        if intersection_start >= intersection_end:
            return 0.0

        intersection = intersection_end - intersection_start
        gt_length = gt_end - gt_start

        return intersection / gt_length if gt_length > 0 else 0.0

    def evaluate_document(self, predictions: List[Dict],
                          ground_truth: List[Dict]) -> Dict:
        """
        Evaluate predictions against ground truth for a single document.

        Args:
            predictions: List of predicted entities from mapping file.
                        Each dict has: type, value, position.start, position.end
            ground_truth: List of ground truth entities.
                         Each dict has: type, value, start, end

        Returns:
            Evaluation results dictionary.
        """
        tp = 0  # True positives
        fp = 0  # False positives
        fn = 0  # False negatives

        matched_gt = set()  # Track which GT entities have been matched
        matched_pred = set()  # Track which predictions have been matched

        tp_details = []
        fp_details = []
        fn_details = []

        # For each prediction, find the best matching ground truth entity
        for pred_idx, pred in enumerate(predictions):
            pred_start = pred.get("position", {}).get("start", 0)
            pred_end = pred.get("position", {}).get("end", 0)
            pred_type = pred.get("type", "")

            best_iou = 0.0
            best_gt_idx = -1

            for gt_idx, gt in enumerate(ground_truth):
                if gt_idx in matched_gt:
                    continue

                gt_start = gt.get("start", 0)
                gt_end = gt.get("end", 0)
                gt_type = gt.get("type", "")

                # Check type match
                if pred_type != gt_type:
                    continue

                # Compute IoU
                iou = self._compute_iou(pred_start, pred_end, gt_start, gt_end)

                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = gt_idx

            if best_iou >= self.iou_threshold and best_gt_idx >= 0:
                tp += 1
                matched_gt.add(best_gt_idx)
                matched_pred.add(pred_idx)
                tp_details.append({
                    "type": pred_type,
                    "predicted": pred.get("original", pred.get("value", "")),
                    "ground_truth": ground_truth[best_gt_idx].get("value", ""),
                    "iou": round(best_iou, 3)
                })
            else:
                fp += 1
                fp_details.append({
                    "type": pred_type,
                    "value": pred.get("original", pred.get("value", "")),
                    "position": f"{pred_start}-{pred_end}",
                    "best_iou": round(best_iou, 3)
                })

        # Find unmatched ground truth entities (false negatives)
        for gt_idx, gt in enumerate(ground_truth):
            if gt_idx not in matched_gt:
                fn += 1
                fn_details.append({
                    "type": gt.get("type", ""),
                    "value": gt.get("value", ""),
                    "position": f"{gt.get('start', 0)}-{gt.get('end', 0)}"
                })

        # Compute metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) > 0 else 0.0)

        total_entities = tp + fn  # Total ground truth entities
        accuracy = tp / total_entities if total_entities > 0 else 1.0

        return {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "accuracy": round(accuracy, 4),
            "tp_details": tp_details,
            "fp_details": fp_details,
            "fn_details": fn_details
        }

    def evaluate_batch(self, mapping_dir: str,
                       ground_truth_dir: str) -> Dict:
        """
        Evaluate all documents in a batch.

        Args:
            mapping_dir: Directory containing mapping JSON files.
            ground_truth_dir: Directory containing ground truth JSON files.

        Returns:
            Aggregate evaluation results.
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_documents": 0,
            "evaluated_documents": 0,
            "aggregate": {},
            "per_type": {},
            "per_document": [],
            "failures": []
        }

        # Find all mapping files
        mapping_files = sorted(glob.glob(os.path.join(mapping_dir, "*_mapping.json")))

        if not mapping_files:
            print(f"[WARN] No mapping files found in {mapping_dir}")
            return results

        results["total_documents"] = len(mapping_files)

        # Aggregate counters
        total_tp = 0
        total_fp = 0
        total_fn = 0

        # Per-type counters
        type_tp = defaultdict(int)
        type_fp = defaultdict(int)
        type_fn = defaultdict(int)

        for mapping_path in mapping_files:
            mapping_name = os.path.basename(mapping_path)
            base_name = mapping_name.replace("_mapping.json", "")

            # Find corresponding ground truth
            gt_path = os.path.join(ground_truth_dir, f"{base_name}_gt.json")

            if not os.path.exists(gt_path):
                results["failures"].append({
                    "file": base_name,
                    "error": f"Ground truth not found: {gt_path}"
                })
                continue

            try:
                # Load mapping
                with open(mapping_path, 'r', encoding='utf-8') as f:
                    mapping = json.load(f)

                # Load ground truth
                with open(gt_path, 'r', encoding='utf-8') as f:
                    gt_data = json.load(f)

                predictions = mapping.get("mappings", [])
                ground_truth = gt_data.get("entities", [])

                # Evaluate
                doc_result = self.evaluate_document(predictions, ground_truth)
                doc_result["document"] = base_name
                doc_result["document_type"] = gt_data.get("document_type", "unknown")

                results["per_document"].append(doc_result)
                results["evaluated_documents"] += 1

                # Accumulate totals
                total_tp += doc_result["true_positives"]
                total_fp += doc_result["false_positives"]
                total_fn += doc_result["false_negatives"]

                # Accumulate per-type
                for tp_item in doc_result["tp_details"]:
                    type_tp[tp_item["type"]] += 1
                for fp_item in doc_result["fp_details"]:
                    type_fp[fp_item["type"]] += 1
                for fn_item in doc_result["fn_details"]:
                    type_fn[fn_item["type"]] += 1

            except Exception as e:
                results["failures"].append({
                    "file": base_name,
                    "error": str(e)
                })

        # Compute aggregate metrics
        agg_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 1.0
        agg_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 1.0
        agg_f1 = (2 * agg_precision * agg_recall / (agg_precision + agg_recall)
                  if (agg_precision + agg_recall) > 0 else 0.0)
        total_gt = total_tp + total_fn
        agg_accuracy = total_tp / total_gt if total_gt > 0 else 1.0

        results["aggregate"] = {
            "true_positives": total_tp,
            "false_positives": total_fp,
            "false_negatives": total_fn,
            "total_ground_truth": total_gt,
            "precision": round(agg_precision, 4),
            "recall": round(agg_recall, 4),
            "f1_score": round(agg_f1, 4),
            "accuracy": round(agg_accuracy, 4)
        }

        # Compute per-type metrics
        all_types = set(list(type_tp.keys()) + list(type_fp.keys()) + list(type_fn.keys()))
        for pii_type in sorted(all_types):
            tp = type_tp[pii_type]
            fp = type_fp[pii_type]
            fn = type_fn[pii_type]

            prec = tp / (tp + fp) if (tp + fp) > 0 else 1.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 1.0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

            results["per_type"][pii_type] = {
                "true_positives": tp,
                "false_positives": fp,
                "false_negatives": fn,
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4)
            }

        return results


def generate_report(results: Dict, output_path: str):
    """
    Generate a human-readable evaluation report in Markdown.

    Args:
        results: Results dictionary from PIIEvaluator.evaluate_batch().
        output_path: Path to save the markdown report.
    """
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    lines = []
    lines.append("# PII Masking Pipeline — Evaluation Report\n")
    lines.append(f"**Generated:** {results.get('timestamp', 'N/A')}\n")
    lines.append(f"**Documents Evaluated:** {results.get('evaluated_documents', 0)} / {results.get('total_documents', 0)}\n")

    # Aggregate metrics
    agg = results.get("aggregate", {})
    lines.append("\n## Overall Metrics\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| **Precision** | {agg.get('precision', 0):.2%} |")
    lines.append(f"| **Recall** | {agg.get('recall', 0):.2%} |")
    lines.append(f"| **F1 Score** | {agg.get('f1_score', 0):.2%} |")
    lines.append(f"| **Accuracy (Recall)** | {agg.get('accuracy', 0):.2%} |")
    lines.append(f"| True Positives | {agg.get('true_positives', 0)} |")
    lines.append(f"| False Positives | {agg.get('false_positives', 0)} |")
    lines.append(f"| False Negatives | {agg.get('false_negatives', 0)} |")
    lines.append(f"| Total Ground Truth Entities | {agg.get('total_ground_truth', 0)} |")

    # Per-type metrics
    per_type = results.get("per_type", {})
    if per_type:
        lines.append("\n## Per-Type Breakdown\n")
        lines.append(f"| PII Type | TP | FP | FN | Precision | Recall | F1 |")
        lines.append(f"|----------|----|----|-----|-----------|--------|-----|")
        for pii_type, metrics in sorted(per_type.items()):
            lines.append(
                f"| {pii_type} | {metrics['true_positives']} | "
                f"{metrics['false_positives']} | {metrics['false_negatives']} | "
                f"{metrics['precision']:.2%} | {metrics['recall']:.2%} | "
                f"{metrics['f1_score']:.2%} |"
            )

    # Per-document summary
    per_doc = results.get("per_document", [])
    if per_doc:
        lines.append("\n## Per-Document Summary\n")
        lines.append(f"| Document | Type | TP | FP | FN | Precision | Recall | F1 |")
        lines.append(f"|----------|------|----|----|----|-----------|--------|-----|")
        for doc in per_doc:
            lines.append(
                f"| {doc['document']} | {doc.get('document_type', '-')} | "
                f"{doc['true_positives']} | {doc['false_positives']} | "
                f"{doc['false_negatives']} | {doc['precision']:.2%} | "
                f"{doc['recall']:.2%} | {doc['f1_score']:.2%} |"
            )

    # Failure analysis — show FN and FP details
    lines.append("\n## Failure Analysis\n")

    # Collect all FN details
    all_fn = []
    all_fp = []
    for doc in per_doc:
        for fn_item in doc.get("fn_details", []):
            all_fn.append({**fn_item, "document": doc["document"]})
        for fp_item in doc.get("fp_details", []):
            all_fp.append({**fp_item, "document": doc["document"]})

    if all_fn:
        lines.append(f"\n### Missed PII (False Negatives) — {len(all_fn)} total\n")
        lines.append(f"| Document | Type | Value | Position |")
        lines.append(f"|----------|------|-------|----------|")
        for fn in all_fn[:30]:  # Show top 30
            val = fn['value'][:40] + '...' if len(fn['value']) > 40 else fn['value']
            lines.append(f"| {fn['document']} | {fn['type']} | `{val}` | {fn['position']} |")
        if len(all_fn) > 30:
            lines.append(f"\n*... and {len(all_fn) - 30} more*\n")

    if all_fp:
        lines.append(f"\n### False Detections (False Positives) — {len(all_fp)} total\n")
        lines.append(f"| Document | Type | Value | Position | Best IoU |")
        lines.append(f"|----------|------|-------|----------|----------|")
        for fp in all_fp[:30]:
            val = fp['value'][:40] + '...' if len(fp['value']) > 40 else fp['value']
            lines.append(
                f"| {fp['document']} | {fp['type']} | `{val}` | "
                f"{fp['position']} | {fp.get('best_iou', 0):.2f} |"
            )

    # Failures
    failures = results.get("failures", [])
    if failures:
        lines.append(f"\n## Processing Failures — {len(failures)}\n")
        for fail in failures:
            lines.append(f"- **{fail['file']}**: {fail['error']}")

    report = '\n'.join(lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate PII masking accuracy")
    parser.add_argument("--mappings", default="sample_data/mappings",
                        help="Directory with mapping JSON files")
    parser.add_argument("--ground-truth", default="sample_data/ground_truth",
                        help="Directory with ground truth JSON files")
    parser.add_argument("--output", default="results/evaluation_report.md",
                        help="Output path for evaluation report")
    parser.add_argument("--iou", type=float, default=0.5,
                        help="IoU threshold for matching (0.0-1.0)")
    args = parser.parse_args()

    evaluator = PIIEvaluator(iou_threshold=args.iou)
    results = evaluator.evaluate_batch(args.mappings, args.ground_truth)

    print(f"\n{'='*50}")
    print(f"  PII MASKING EVALUATION RESULTS")
    print(f"{'='*50}")

    agg = results.get("aggregate", {})
    print(f"\n  Precision:  {agg.get('precision', 0):.2%}")
    print(f"  Recall:     {agg.get('recall', 0):.2%}")
    print(f"  F1 Score:   {agg.get('f1_score', 0):.2%}")
    print(f"  Accuracy:   {agg.get('accuracy', 0):.2%}")
    print(f"\n  TP: {agg.get('true_positives', 0)} | "
          f"FP: {agg.get('false_positives', 0)} | "
          f"FN: {agg.get('false_negatives', 0)}")

    report = generate_report(results, args.output)
    print(f"\n[FILE] Full report saved to: {args.output}")

    # Save raw results JSON
    json_path = args.output.replace('.md', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"[DATA] Raw results saved to: {json_path}")
