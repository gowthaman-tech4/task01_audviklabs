# PII Masking Pipeline — Evaluation Report

**Generated:** 2026-06-09T08:06:05.053520

**Documents Evaluated:** 504 / 504


## Overall Metrics

| Metric | Value |
|--------|-------|
| **Precision** | 42.19% |
| **Recall** | 82.78% |
| **F1 Score** | 55.89% |
| **Accuracy (Recall)** | 82.78% |
| True Positives | 3273 |
| False Positives | 4485 |
| False Negatives | 681 |
| Total Ground Truth Entities | 3954 |

## Per-Type Breakdown

| PII Type | TP | FP | FN | Precision | Recall | F1 |
|----------|----|----|-----|-----------|--------|-----|
| AADHAAR | 124 | 126 | 2 | 49.60% | 98.41% | 65.96% |
| ACCOUNT_NUMBER | 204 | 118 | 132 | 63.35% | 60.71% | 62.01% |
| ADDRESS | 383 | 505 | 289 | 43.13% | 56.99% | 49.10% |
| CREDIT_CARD | 0 | 0 | 84 | 100.00% | 0.00% | 0.00% |
| DATE_OF_BIRTH | 378 | 12 | 0 | 96.92% | 100.00% | 98.44% |
| EMAIL | 506 | 174 | 0 | 74.41% | 100.00% | 85.33% |
| IFSC_CODE | 42 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| ORGANIZATION | 0 | 1984 | 168 | 0.00% | 0.00% | 0.00% |
| PAN | 210 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| PERSON_NAME | 711 | 1385 | 5 | 33.92% | 99.30% | 50.57% |
| PHONE | 506 | 97 | 0 | 83.91% | 100.00% | 91.25% |
| POLICY_NUMBER | 0 | 84 | 0 | 0.00% | 100.00% | 0.00% |
| SSN | 209 | 0 | 1 | 100.00% | 99.52% | 99.76% |

## Per-Document Summary

| Document | Type | TP | FP | FN | Precision | Recall | F1 |
|----------|------|----|----|----|-----------|--------|-----|
| bank_statement_in_001 | bank_statement | 7 | 5 | 1 | 58.33% | 87.50% | 70.00% |
| bank_statement_in_002 | bank_statement | 7 | 6 | 1 | 53.85% | 87.50% | 66.67% |
| bank_statement_in_003 | bank_statement | 6 | 4 | 2 | 60.00% | 75.00% | 66.67% |
| bank_statement_in_004 | bank_statement | 6 | 9 | 2 | 40.00% | 75.00% | 52.17% |
| bank_statement_in_005 | bank_statement | 6 | 3 | 2 | 66.67% | 75.00% | 70.59% |
| bank_statement_in_006 | bank_statement | 7 | 3 | 1 | 70.00% | 87.50% | 77.78% |
| bank_statement_in_007 | bank_statement | 8 | 7 | 0 | 53.33% | 100.00% | 69.57% |
| bank_statement_in_008 | bank_statement | 7 | 7 | 1 | 50.00% | 87.50% | 63.64% |
| bank_statement_in_009 | bank_statement | 7 | 10 | 1 | 41.18% | 87.50% | 56.00% |
| bank_statement_in_010 | bank_statement | 7 | 11 | 1 | 38.89% | 87.50% | 53.85% |
| bank_statement_in_011 | bank_statement | 6 | 6 | 2 | 50.00% | 75.00% | 60.00% |
| bank_statement_in_012 | bank_statement | 7 | 10 | 1 | 41.18% | 87.50% | 56.00% |
| bank_statement_in_013 | bank_statement | 7 | 4 | 1 | 63.64% | 87.50% | 73.68% |
| bank_statement_in_014 | bank_statement | 6 | 7 | 2 | 46.15% | 75.00% | 57.14% |
| bank_statement_in_015 | bank_statement | 7 | 5 | 1 | 58.33% | 87.50% | 70.00% |
| bank_statement_in_016 | bank_statement | 7 | 7 | 1 | 50.00% | 87.50% | 63.64% |
| bank_statement_in_017 | bank_statement | 7 | 5 | 1 | 58.33% | 87.50% | 70.00% |
| bank_statement_in_018 | bank_statement | 8 | 2 | 0 | 80.00% | 100.00% | 88.89% |
| bank_statement_in_019 | bank_statement | 6 | 8 | 2 | 42.86% | 75.00% | 54.55% |
| bank_statement_in_020 | bank_statement | 7 | 10 | 1 | 41.18% | 87.50% | 56.00% |
| bank_statement_in_021 | bank_statement | 7 | 4 | 1 | 63.64% | 87.50% | 73.68% |
| bank_statement_in_022 | bank_statement | 6 | 7 | 2 | 46.15% | 75.00% | 57.14% |
| bank_statement_in_023 | bank_statement | 7 | 5 | 1 | 58.33% | 87.50% | 70.00% |
| bank_statement_in_024 | bank_statement | 7 | 8 | 1 | 46.67% | 87.50% | 60.87% |
| bank_statement_in_025 | bank_statement | 6 | 8 | 2 | 42.86% | 75.00% | 54.55% |
| bank_statement_in_026 | bank_statement | 7 | 2 | 1 | 77.78% | 87.50% | 82.35% |
| bank_statement_in_027 | bank_statement | 7 | 5 | 1 | 58.33% | 87.50% | 70.00% |
| bank_statement_in_028 | bank_statement | 7 | 6 | 1 | 53.85% | 87.50% | 66.67% |
| bank_statement_in_029 | bank_statement | 8 | 7 | 0 | 53.33% | 100.00% | 69.57% |
| bank_statement_in_030 | bank_statement | 6 | 10 | 2 | 37.50% | 75.00% | 50.00% |
| bank_statement_in_031 | bank_statement | 7 | 7 | 1 | 50.00% | 87.50% | 63.64% |
| bank_statement_in_032 | bank_statement | 6 | 9 | 2 | 40.00% | 75.00% | 52.17% |
| bank_statement_in_033 | bank_statement | 6 | 10 | 2 | 37.50% | 75.00% | 50.00% |
| bank_statement_in_034 | bank_statement | 7 | 7 | 1 | 50.00% | 87.50% | 63.64% |
| bank_statement_in_035 | bank_statement | 7 | 7 | 1 | 50.00% | 87.50% | 63.64% |
| bank_statement_in_036 | bank_statement | 7 | 4 | 1 | 63.64% | 87.50% | 73.68% |
| bank_statement_in_037 | bank_statement | 6 | 4 | 2 | 60.00% | 75.00% | 66.67% |
| bank_statement_in_038 | bank_statement | 7 | 6 | 1 | 53.85% | 87.50% | 66.67% |
| bank_statement_in_039 | bank_statement | 7 | 5 | 1 | 58.33% | 87.50% | 70.00% |
| bank_statement_in_040 | bank_statement | 6 | 9 | 2 | 40.00% | 75.00% | 52.17% |
| bank_statement_in_041 | bank_statement | 7 | 2 | 1 | 77.78% | 87.50% | 82.35% |
| bank_statement_in_042 | bank_statement | 7 | 3 | 1 | 70.00% | 87.50% | 77.78% |
| bank_statement_us_001 | bank_statement | 6 | 2 | 1 | 75.00% | 85.71% | 80.00% |
| bank_statement_us_002 | bank_statement | 6 | 6 | 1 | 50.00% | 85.71% | 63.16% |
| bank_statement_us_003 | bank_statement | 6 | 3 | 1 | 66.67% | 85.71% | 75.00% |
| bank_statement_us_004 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_005 | bank_statement | 6 | 11 | 1 | 35.29% | 85.71% | 50.00% |
| bank_statement_us_006 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_007 | bank_statement | 6 | 10 | 1 | 37.50% | 85.71% | 52.17% |
| bank_statement_us_008 | bank_statement | 6 | 10 | 1 | 37.50% | 85.71% | 52.17% |
| bank_statement_us_009 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_010 | bank_statement | 6 | 7 | 1 | 46.15% | 85.71% | 60.00% |
| bank_statement_us_011 | bank_statement | 6 | 3 | 1 | 66.67% | 85.71% | 75.00% |
| bank_statement_us_012 | bank_statement | 6 | 5 | 1 | 54.55% | 85.71% | 66.67% |
| bank_statement_us_013 | bank_statement | 6 | 6 | 1 | 50.00% | 85.71% | 63.16% |
| bank_statement_us_014 | bank_statement | 6 | 1 | 1 | 85.71% | 85.71% | 85.71% |
| bank_statement_us_015 | bank_statement | 6 | 5 | 1 | 54.55% | 85.71% | 66.67% |
| bank_statement_us_016 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_017 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_018 | bank_statement | 6 | 3 | 1 | 66.67% | 85.71% | 75.00% |
| bank_statement_us_019 | bank_statement | 6 | 7 | 1 | 46.15% | 85.71% | 60.00% |
| bank_statement_us_020 | bank_statement | 6 | 6 | 1 | 50.00% | 85.71% | 63.16% |
| bank_statement_us_021 | bank_statement | 6 | 12 | 1 | 33.33% | 85.71% | 48.00% |
| bank_statement_us_022 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_023 | bank_statement | 6 | 1 | 1 | 85.71% | 85.71% | 85.71% |
| bank_statement_us_024 | bank_statement | 6 | 7 | 1 | 46.15% | 85.71% | 60.00% |
| bank_statement_us_025 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_026 | bank_statement | 6 | 3 | 1 | 66.67% | 85.71% | 75.00% |
| bank_statement_us_027 | bank_statement | 6 | 1 | 1 | 85.71% | 85.71% | 85.71% |
| bank_statement_us_028 | bank_statement | 6 | 12 | 1 | 33.33% | 85.71% | 48.00% |
| bank_statement_us_029 | bank_statement | 6 | 6 | 1 | 50.00% | 85.71% | 63.16% |
| bank_statement_us_030 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_031 | bank_statement | 6 | 3 | 1 | 66.67% | 85.71% | 75.00% |
| bank_statement_us_032 | bank_statement | 6 | 3 | 1 | 66.67% | 85.71% | 75.00% |
| bank_statement_us_033 | bank_statement | 6 | 5 | 1 | 54.55% | 85.71% | 66.67% |
| bank_statement_us_034 | bank_statement | 6 | 9 | 1 | 40.00% | 85.71% | 54.55% |
| bank_statement_us_035 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_036 | bank_statement | 6 | 5 | 1 | 54.55% | 85.71% | 66.67% |
| bank_statement_us_037 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_038 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_039 | bank_statement | 6 | 4 | 1 | 60.00% | 85.71% | 70.59% |
| bank_statement_us_040 | bank_statement | 6 | 6 | 1 | 50.00% | 85.71% | 63.16% |
| bank_statement_us_041 | bank_statement | 6 | 2 | 1 | 75.00% | 85.71% | 80.00% |
| bank_statement_us_042 | bank_statement | 6 | 2 | 1 | 75.00% | 85.71% | 80.00% |
| brokerage_statement_in_001 | brokerage_statement | 5 | 9 | 2 | 35.71% | 71.43% | 47.62% |
| brokerage_statement_in_002 | brokerage_statement | 5 | 9 | 2 | 35.71% | 71.43% | 47.62% |
| brokerage_statement_in_003 | brokerage_statement | 5 | 11 | 2 | 31.25% | 71.43% | 43.48% |
| brokerage_statement_in_004 | brokerage_statement | 5 | 8 | 2 | 38.46% | 71.43% | 50.00% |
| brokerage_statement_in_005 | brokerage_statement | 5 | 9 | 2 | 35.71% | 71.43% | 47.62% |
| brokerage_statement_in_006 | brokerage_statement | 5 | 14 | 2 | 26.32% | 71.43% | 38.46% |
| brokerage_statement_in_007 | brokerage_statement | 6 | 7 | 1 | 46.15% | 85.71% | 60.00% |
| brokerage_statement_in_008 | brokerage_statement | 5 | 11 | 2 | 31.25% | 71.43% | 43.48% |
| brokerage_statement_in_009 | brokerage_statement | 6 | 9 | 1 | 40.00% | 85.71% | 54.55% |
| brokerage_statement_in_010 | brokerage_statement | 5 | 10 | 2 | 33.33% | 71.43% | 45.45% |
| brokerage_statement_in_011 | brokerage_statement | 5 | 8 | 2 | 38.46% | 71.43% | 50.00% |
| brokerage_statement_in_012 | brokerage_statement | 5 | 10 | 2 | 33.33% | 71.43% | 45.45% |
| brokerage_statement_in_013 | brokerage_statement | 6 | 9 | 1 | 40.00% | 85.71% | 54.55% |
| brokerage_statement_in_014 | brokerage_statement | 6 | 8 | 1 | 42.86% | 85.71% | 57.14% |
| brokerage_statement_in_015 | brokerage_statement | 6 | 8 | 1 | 42.86% | 85.71% | 57.14% |
| brokerage_statement_in_016 | brokerage_statement | 5 | 9 | 2 | 35.71% | 71.43% | 47.62% |
| brokerage_statement_in_017 | brokerage_statement | 5 | 13 | 2 | 27.78% | 71.43% | 40.00% |
| brokerage_statement_in_018 | brokerage_statement | 5 | 11 | 2 | 31.25% | 71.43% | 43.48% |
| brokerage_statement_in_019 | brokerage_statement | 6 | 5 | 1 | 54.55% | 85.71% | 66.67% |
| brokerage_statement_in_020 | brokerage_statement | 5 | 10 | 2 | 33.33% | 71.43% | 45.45% |
| brokerage_statement_in_021 | brokerage_statement | 5 | 12 | 2 | 29.41% | 71.43% | 41.67% |
| brokerage_statement_in_022 | brokerage_statement | 6 | 9 | 1 | 40.00% | 85.71% | 54.55% |
| brokerage_statement_in_023 | brokerage_statement | 5 | 9 | 2 | 35.71% | 71.43% | 47.62% |
| brokerage_statement_in_024 | brokerage_statement | 5 | 11 | 2 | 31.25% | 71.43% | 43.48% |
| brokerage_statement_in_025 | brokerage_statement | 6 | 8 | 1 | 42.86% | 85.71% | 57.14% |
| brokerage_statement_in_026 | brokerage_statement | 6 | 6 | 1 | 50.00% | 85.71% | 63.16% |
| brokerage_statement_in_027 | brokerage_statement | 6 | 5 | 1 | 54.55% | 85.71% | 66.67% |
| brokerage_statement_in_028 | brokerage_statement | 5 | 13 | 2 | 27.78% | 71.43% | 40.00% |
| brokerage_statement_in_029 | brokerage_statement | 6 | 7 | 1 | 46.15% | 85.71% | 60.00% |
| brokerage_statement_in_030 | brokerage_statement | 5 | 12 | 2 | 29.41% | 71.43% | 41.67% |
| brokerage_statement_in_031 | brokerage_statement | 6 | 11 | 1 | 35.29% | 85.71% | 50.00% |
| brokerage_statement_in_032 | brokerage_statement | 5 | 7 | 2 | 41.67% | 71.43% | 52.63% |
| brokerage_statement_in_033 | brokerage_statement | 5 | 12 | 2 | 29.41% | 71.43% | 41.67% |
| brokerage_statement_in_034 | brokerage_statement | 6 | 9 | 1 | 40.00% | 85.71% | 54.55% |
| brokerage_statement_in_035 | brokerage_statement | 5 | 9 | 2 | 35.71% | 71.43% | 47.62% |
| brokerage_statement_in_036 | brokerage_statement | 6 | 10 | 1 | 37.50% | 85.71% | 52.17% |
| brokerage_statement_in_037 | brokerage_statement | 6 | 10 | 1 | 37.50% | 85.71% | 52.17% |
| brokerage_statement_in_038 | brokerage_statement | 5 | 8 | 2 | 38.46% | 71.43% | 50.00% |
| brokerage_statement_in_039 | brokerage_statement | 5 | 11 | 2 | 31.25% | 71.43% | 43.48% |
| brokerage_statement_in_040 | brokerage_statement | 5 | 8 | 2 | 38.46% | 71.43% | 50.00% |
| brokerage_statement_in_041 | brokerage_statement | 5 | 6 | 2 | 45.45% | 71.43% | 55.56% |
| brokerage_statement_in_042 | brokerage_statement | 6 | 8 | 1 | 42.86% | 85.71% | 57.14% |
| brokerage_statement_us_001 | brokerage_statement | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| brokerage_statement_us_002 | brokerage_statement | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| brokerage_statement_us_003 | brokerage_statement | 5 | 7 | 1 | 41.67% | 83.33% | 55.56% |
| brokerage_statement_us_004 | brokerage_statement | 5 | 7 | 1 | 41.67% | 83.33% | 55.56% |
| brokerage_statement_us_005 | brokerage_statement | 5 | 6 | 1 | 45.45% | 83.33% | 58.82% |
| brokerage_statement_us_006 | brokerage_statement | 5 | 6 | 1 | 45.45% | 83.33% | 58.82% |
| brokerage_statement_us_007 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_008 | brokerage_statement | 5 | 6 | 1 | 45.45% | 83.33% | 58.82% |
| brokerage_statement_us_009 | brokerage_statement | 5 | 7 | 1 | 41.67% | 83.33% | 55.56% |
| brokerage_statement_us_010 | brokerage_statement | 5 | 6 | 1 | 45.45% | 83.33% | 58.82% |
| brokerage_statement_us_011 | brokerage_statement | 5 | 6 | 1 | 45.45% | 83.33% | 58.82% |
| brokerage_statement_us_012 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_013 | brokerage_statement | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| brokerage_statement_us_014 | brokerage_statement | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| brokerage_statement_us_015 | brokerage_statement | 6 | 4 | 0 | 60.00% | 100.00% | 75.00% |
| brokerage_statement_us_016 | brokerage_statement | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| brokerage_statement_us_017 | brokerage_statement | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| brokerage_statement_us_018 | brokerage_statement | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| brokerage_statement_us_019 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_020 | brokerage_statement | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| brokerage_statement_us_021 | brokerage_statement | 5 | 10 | 1 | 33.33% | 83.33% | 47.62% |
| brokerage_statement_us_022 | brokerage_statement | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| brokerage_statement_us_023 | brokerage_statement | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| brokerage_statement_us_024 | brokerage_statement | 5 | 11 | 1 | 31.25% | 83.33% | 45.45% |
| brokerage_statement_us_025 | brokerage_statement | 5 | 11 | 1 | 31.25% | 83.33% | 45.45% |
| brokerage_statement_us_026 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_027 | brokerage_statement | 5 | 4 | 1 | 55.56% | 83.33% | 66.67% |
| brokerage_statement_us_028 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_029 | brokerage_statement | 5 | 7 | 1 | 41.67% | 83.33% | 55.56% |
| brokerage_statement_us_030 | brokerage_statement | 5 | 11 | 1 | 31.25% | 83.33% | 45.45% |
| brokerage_statement_us_031 | brokerage_statement | 5 | 7 | 1 | 41.67% | 83.33% | 55.56% |
| brokerage_statement_us_032 | brokerage_statement | 6 | 5 | 0 | 54.55% | 100.00% | 70.59% |
| brokerage_statement_us_033 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_034 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_035 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| brokerage_statement_us_036 | brokerage_statement | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| brokerage_statement_us_037 | brokerage_statement | 5 | 4 | 1 | 55.56% | 83.33% | 66.67% |
| brokerage_statement_us_038 | brokerage_statement | 5 | 6 | 1 | 45.45% | 83.33% | 58.82% |
| brokerage_statement_us_039 | brokerage_statement | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| brokerage_statement_us_040 | brokerage_statement | 5 | 6 | 1 | 45.45% | 83.33% | 58.82% |
| brokerage_statement_us_041 | brokerage_statement | 5 | 10 | 1 | 33.33% | 83.33% | 47.62% |
| brokerage_statement_us_042 | brokerage_statement | 5 | 5 | 1 | 50.00% | 83.33% | 62.50% |
| credit_card_statement_in_001 | credit_card_statement | 3 | 12 | 2 | 20.00% | 60.00% | 30.00% |
| credit_card_statement_in_002 | credit_card_statement | 3 | 9 | 2 | 25.00% | 60.00% | 35.29% |
| credit_card_statement_in_003 | credit_card_statement | 3 | 6 | 2 | 33.33% | 60.00% | 42.86% |
| credit_card_statement_in_004 | credit_card_statement | 3 | 13 | 2 | 18.75% | 60.00% | 28.57% |
| credit_card_statement_in_005 | credit_card_statement | 3 | 13 | 2 | 18.75% | 60.00% | 28.57% |
| credit_card_statement_in_006 | credit_card_statement | 3 | 11 | 2 | 21.43% | 60.00% | 31.58% |
| credit_card_statement_in_007 | credit_card_statement | 3 | 14 | 2 | 17.65% | 60.00% | 27.27% |
| credit_card_statement_in_008 | credit_card_statement | 3 | 7 | 2 | 30.00% | 60.00% | 40.00% |
| credit_card_statement_in_009 | credit_card_statement | 3 | 12 | 2 | 20.00% | 60.00% | 30.00% |
| credit_card_statement_in_010 | credit_card_statement | 3 | 10 | 2 | 23.08% | 60.00% | 33.33% |
| credit_card_statement_in_011 | credit_card_statement | 3 | 12 | 2 | 20.00% | 60.00% | 30.00% |
| credit_card_statement_in_012 | credit_card_statement | 3 | 14 | 2 | 17.65% | 60.00% | 27.27% |
| credit_card_statement_in_013 | credit_card_statement | 3 | 18 | 2 | 14.29% | 60.00% | 23.08% |
| credit_card_statement_in_014 | credit_card_statement | 3 | 13 | 2 | 18.75% | 60.00% | 28.57% |
| credit_card_statement_in_015 | credit_card_statement | 3 | 7 | 2 | 30.00% | 60.00% | 40.00% |
| credit_card_statement_in_016 | credit_card_statement | 4 | 7 | 1 | 36.36% | 80.00% | 50.00% |
| credit_card_statement_in_017 | credit_card_statement | 3 | 11 | 2 | 21.43% | 60.00% | 31.58% |
| credit_card_statement_in_018 | credit_card_statement | 3 | 6 | 2 | 33.33% | 60.00% | 42.86% |
| credit_card_statement_in_019 | credit_card_statement | 3 | 7 | 2 | 30.00% | 60.00% | 40.00% |
| credit_card_statement_in_020 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_in_021 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_in_022 | credit_card_statement | 3 | 12 | 2 | 20.00% | 60.00% | 30.00% |
| credit_card_statement_in_023 | credit_card_statement | 3 | 11 | 2 | 21.43% | 60.00% | 31.58% |
| credit_card_statement_in_024 | credit_card_statement | 4 | 8 | 1 | 33.33% | 80.00% | 47.06% |
| credit_card_statement_in_025 | credit_card_statement | 4 | 7 | 1 | 36.36% | 80.00% | 50.00% |
| credit_card_statement_in_026 | credit_card_statement | 3 | 11 | 2 | 21.43% | 60.00% | 31.58% |
| credit_card_statement_in_027 | credit_card_statement | 3 | 9 | 2 | 25.00% | 60.00% | 35.29% |
| credit_card_statement_in_028 | credit_card_statement | 3 | 10 | 2 | 23.08% | 60.00% | 33.33% |
| credit_card_statement_in_029 | credit_card_statement | 3 | 10 | 2 | 23.08% | 60.00% | 33.33% |
| credit_card_statement_in_030 | credit_card_statement | 3 | 14 | 2 | 17.65% | 60.00% | 27.27% |
| credit_card_statement_in_031 | credit_card_statement | 3 | 7 | 2 | 30.00% | 60.00% | 40.00% |
| credit_card_statement_in_032 | credit_card_statement | 3 | 11 | 2 | 21.43% | 60.00% | 31.58% |
| credit_card_statement_in_033 | credit_card_statement | 3 | 12 | 2 | 20.00% | 60.00% | 30.00% |
| credit_card_statement_in_034 | credit_card_statement | 3 | 15 | 2 | 16.67% | 60.00% | 26.09% |
| credit_card_statement_in_035 | credit_card_statement | 3 | 7 | 2 | 30.00% | 60.00% | 40.00% |
| credit_card_statement_in_036 | credit_card_statement | 3 | 17 | 2 | 15.00% | 60.00% | 24.00% |
| credit_card_statement_in_037 | credit_card_statement | 4 | 7 | 1 | 36.36% | 80.00% | 50.00% |
| credit_card_statement_in_038 | credit_card_statement | 3 | 7 | 2 | 30.00% | 60.00% | 40.00% |
| credit_card_statement_in_039 | credit_card_statement | 3 | 15 | 2 | 16.67% | 60.00% | 26.09% |
| credit_card_statement_in_040 | credit_card_statement | 3 | 14 | 2 | 17.65% | 60.00% | 27.27% |
| credit_card_statement_in_041 | credit_card_statement | 3 | 10 | 2 | 23.08% | 60.00% | 33.33% |
| credit_card_statement_in_042 | credit_card_statement | 3 | 16 | 2 | 15.79% | 60.00% | 25.00% |
| credit_card_statement_us_001 | credit_card_statement | 4 | 6 | 1 | 40.00% | 80.00% | 53.33% |
| credit_card_statement_us_002 | credit_card_statement | 4 | 11 | 1 | 26.67% | 80.00% | 40.00% |
| credit_card_statement_us_003 | credit_card_statement | 4 | 8 | 1 | 33.33% | 80.00% | 47.06% |
| credit_card_statement_us_004 | credit_card_statement | 4 | 10 | 1 | 28.57% | 80.00% | 42.11% |
| credit_card_statement_us_005 | credit_card_statement | 4 | 5 | 1 | 44.44% | 80.00% | 57.14% |
| credit_card_statement_us_006 | credit_card_statement | 4 | 6 | 1 | 40.00% | 80.00% | 53.33% |
| credit_card_statement_us_007 | credit_card_statement | 4 | 18 | 1 | 18.18% | 80.00% | 29.63% |
| credit_card_statement_us_008 | credit_card_statement | 4 | 11 | 1 | 26.67% | 80.00% | 40.00% |
| credit_card_statement_us_009 | credit_card_statement | 4 | 8 | 1 | 33.33% | 80.00% | 47.06% |
| credit_card_statement_us_010 | credit_card_statement | 4 | 4 | 1 | 50.00% | 80.00% | 61.54% |
| credit_card_statement_us_011 | credit_card_statement | 4 | 11 | 1 | 26.67% | 80.00% | 40.00% |
| credit_card_statement_us_012 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_013 | credit_card_statement | 4 | 15 | 1 | 21.05% | 80.00% | 33.33% |
| credit_card_statement_us_014 | credit_card_statement | 4 | 4 | 1 | 50.00% | 80.00% | 61.54% |
| credit_card_statement_us_015 | credit_card_statement | 4 | 6 | 1 | 40.00% | 80.00% | 53.33% |
| credit_card_statement_us_016 | credit_card_statement | 4 | 11 | 1 | 26.67% | 80.00% | 40.00% |
| credit_card_statement_us_017 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_018 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_019 | credit_card_statement | 4 | 8 | 1 | 33.33% | 80.00% | 47.06% |
| credit_card_statement_us_020 | credit_card_statement | 4 | 11 | 1 | 26.67% | 80.00% | 40.00% |
| credit_card_statement_us_021 | credit_card_statement | 4 | 10 | 1 | 28.57% | 80.00% | 42.11% |
| credit_card_statement_us_022 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_023 | credit_card_statement | 4 | 15 | 1 | 21.05% | 80.00% | 33.33% |
| credit_card_statement_us_024 | credit_card_statement | 4 | 7 | 1 | 36.36% | 80.00% | 50.00% |
| credit_card_statement_us_025 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_026 | credit_card_statement | 4 | 8 | 1 | 33.33% | 80.00% | 47.06% |
| credit_card_statement_us_027 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_028 | credit_card_statement | 4 | 6 | 1 | 40.00% | 80.00% | 53.33% |
| credit_card_statement_us_029 | credit_card_statement | 4 | 11 | 1 | 26.67% | 80.00% | 40.00% |
| credit_card_statement_us_030 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_031 | credit_card_statement | 4 | 16 | 1 | 20.00% | 80.00% | 32.00% |
| credit_card_statement_us_032 | credit_card_statement | 4 | 9 | 1 | 30.77% | 80.00% | 44.44% |
| credit_card_statement_us_033 | credit_card_statement | 4 | 20 | 1 | 16.67% | 80.00% | 27.59% |
| credit_card_statement_us_034 | credit_card_statement | 4 | 10 | 1 | 28.57% | 80.00% | 42.11% |
| credit_card_statement_us_035 | credit_card_statement | 4 | 7 | 1 | 36.36% | 80.00% | 50.00% |
| credit_card_statement_us_036 | credit_card_statement | 4 | 7 | 1 | 36.36% | 80.00% | 50.00% |
| credit_card_statement_us_037 | credit_card_statement | 4 | 16 | 1 | 20.00% | 80.00% | 32.00% |
| credit_card_statement_us_038 | credit_card_statement | 4 | 15 | 1 | 21.05% | 80.00% | 33.33% |
| credit_card_statement_us_039 | credit_card_statement | 4 | 17 | 1 | 19.05% | 80.00% | 30.77% |
| credit_card_statement_us_040 | credit_card_statement | 4 | 15 | 1 | 21.05% | 80.00% | 33.33% |
| credit_card_statement_us_041 | credit_card_statement | 4 | 15 | 1 | 21.05% | 80.00% | 33.33% |
| credit_card_statement_us_042 | credit_card_statement | 4 | 18 | 1 | 18.18% | 80.00% | 29.63% |
| insurance_letter_in_001 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_002 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_003 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_004 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_in_005 | insurance_letter | 8 | 13 | 2 | 38.10% | 80.00% | 51.61% |
| insurance_letter_in_006 | insurance_letter | 9 | 10 | 1 | 47.37% | 90.00% | 62.07% |
| insurance_letter_in_007 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_008 | insurance_letter | 9 | 10 | 1 | 47.37% | 90.00% | 62.07% |
| insurance_letter_in_009 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_010 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_in_011 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_012 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_013 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_014 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_in_015 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_in_016 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_017 | insurance_letter | 9 | 13 | 1 | 40.91% | 90.00% | 56.25% |
| insurance_letter_in_018 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_019 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_020 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_021 | insurance_letter | 9 | 10 | 1 | 47.37% | 90.00% | 62.07% |
| insurance_letter_in_022 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_023 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_024 | insurance_letter | 10 | 10 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_in_025 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_026 | insurance_letter | 9 | 13 | 1 | 40.91% | 90.00% | 56.25% |
| insurance_letter_in_027 | insurance_letter | 9 | 10 | 1 | 47.37% | 90.00% | 62.07% |
| insurance_letter_in_028 | insurance_letter | 9 | 10 | 1 | 47.37% | 90.00% | 62.07% |
| insurance_letter_in_029 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_030 | insurance_letter | 10 | 10 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_in_031 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_in_032 | insurance_letter | 8 | 12 | 2 | 40.00% | 80.00% | 53.33% |
| insurance_letter_in_033 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_034 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_035 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_036 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_037 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_038 | insurance_letter | 9 | 12 | 1 | 42.86% | 90.00% | 58.06% |
| insurance_letter_in_039 | insurance_letter | 9 | 11 | 1 | 45.00% | 90.00% | 60.00% |
| insurance_letter_in_040 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_in_041 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_in_042 | insurance_letter | 10 | 9 | 0 | 52.63% | 100.00% | 68.97% |
| insurance_letter_us_001 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_002 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_003 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_004 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_005 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_006 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_007 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_008 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_009 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_010 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_011 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_012 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_013 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_014 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_015 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_016 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_017 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_018 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_019 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_020 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_021 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_022 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_023 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_024 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_025 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_026 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_027 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_028 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_029 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_030 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_031 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_032 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_033 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_034 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_035 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_036 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_037 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_038 | insurance_letter | 9 | 10 | 0 | 47.37% | 100.00% | 64.29% |
| insurance_letter_us_039 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_040 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| insurance_letter_us_041 | insurance_letter | 8 | 10 | 1 | 44.44% | 88.89% | 59.26% |
| insurance_letter_us_042 | insurance_letter | 9 | 9 | 0 | 50.00% | 100.00% | 66.67% |
| loan_agreement_in_001 | loan_agreement | 10 | 11 | 3 | 47.62% | 76.92% | 58.82% |
| loan_agreement_in_002 | loan_agreement | 7 | 11 | 3 | 38.89% | 70.00% | 50.00% |
| loan_agreement_in_003 | loan_agreement | 10 | 12 | 3 | 45.45% | 76.92% | 57.14% |
| loan_agreement_in_004 | loan_agreement | 10 | 11 | 3 | 47.62% | 76.92% | 58.82% |
| loan_agreement_in_005 | loan_agreement | 11 | 8 | 2 | 57.89% | 84.62% | 68.75% |
| loan_agreement_in_006 | loan_agreement | 10 | 13 | 3 | 43.48% | 76.92% | 55.56% |
| loan_agreement_in_007 | loan_agreement | 10 | 11 | 3 | 47.62% | 76.92% | 58.82% |
| loan_agreement_in_008 | loan_agreement | 10 | 13 | 3 | 43.48% | 76.92% | 55.56% |
| loan_agreement_in_009 | loan_agreement | 10 | 12 | 3 | 45.45% | 76.92% | 57.14% |
| loan_agreement_in_010 | loan_agreement | 10 | 10 | 3 | 50.00% | 76.92% | 60.61% |
| loan_agreement_in_011 | loan_agreement | 10 | 12 | 3 | 45.45% | 76.92% | 57.14% |
| loan_agreement_in_012 | loan_agreement | 9 | 7 | 1 | 56.25% | 90.00% | 69.23% |
| loan_agreement_in_013 | loan_agreement | 7 | 12 | 3 | 36.84% | 70.00% | 48.28% |
| loan_agreement_in_014 | loan_agreement | 7 | 12 | 3 | 36.84% | 70.00% | 48.28% |
| loan_agreement_in_015 | loan_agreement | 11 | 10 | 2 | 52.38% | 84.62% | 64.71% |
| loan_agreement_in_016 | loan_agreement | 8 | 9 | 2 | 47.06% | 80.00% | 59.26% |
| loan_agreement_in_017 | loan_agreement | 11 | 9 | 2 | 55.00% | 84.62% | 66.67% |
| loan_agreement_in_018 | loan_agreement | 11 | 9 | 2 | 55.00% | 84.62% | 66.67% |
| loan_agreement_in_019 | loan_agreement | 11 | 10 | 2 | 52.38% | 84.62% | 64.71% |
| loan_agreement_in_020 | loan_agreement | 7 | 11 | 3 | 38.89% | 70.00% | 50.00% |
| loan_agreement_in_021 | loan_agreement | 10 | 12 | 3 | 45.45% | 76.92% | 57.14% |
| loan_agreement_in_022 | loan_agreement | 7 | 9 | 3 | 43.75% | 70.00% | 53.85% |
| loan_agreement_in_023 | loan_agreement | 10 | 14 | 3 | 41.67% | 76.92% | 54.05% |
| loan_agreement_in_024 | loan_agreement | 8 | 8 | 2 | 50.00% | 80.00% | 61.54% |
| loan_agreement_in_025 | loan_agreement | 7 | 11 | 3 | 38.89% | 70.00% | 50.00% |
| loan_agreement_in_026 | loan_agreement | 10 | 12 | 3 | 45.45% | 76.92% | 57.14% |
| loan_agreement_in_027 | loan_agreement | 7 | 11 | 3 | 38.89% | 70.00% | 50.00% |
| loan_agreement_in_028 | loan_agreement | 9 | 7 | 1 | 56.25% | 90.00% | 69.23% |
| loan_agreement_in_029 | loan_agreement | 10 | 10 | 3 | 50.00% | 76.92% | 60.61% |
| loan_agreement_in_030 | loan_agreement | 7 | 12 | 3 | 36.84% | 70.00% | 48.28% |
| loan_agreement_in_031 | loan_agreement | 7 | 13 | 3 | 35.00% | 70.00% | 46.67% |
| loan_agreement_in_032 | loan_agreement | 7 | 11 | 3 | 38.89% | 70.00% | 50.00% |
| loan_agreement_in_033 | loan_agreement | 7 | 11 | 3 | 38.89% | 70.00% | 50.00% |
| loan_agreement_in_034 | loan_agreement | 10 | 11 | 3 | 47.62% | 76.92% | 58.82% |
| loan_agreement_in_035 | loan_agreement | 10 | 11 | 3 | 47.62% | 76.92% | 58.82% |
| loan_agreement_in_036 | loan_agreement | 10 | 11 | 3 | 47.62% | 76.92% | 58.82% |
| loan_agreement_in_037 | loan_agreement | 10 | 12 | 3 | 45.45% | 76.92% | 57.14% |
| loan_agreement_in_038 | loan_agreement | 10 | 11 | 3 | 47.62% | 76.92% | 58.82% |
| loan_agreement_in_039 | loan_agreement | 10 | 13 | 3 | 43.48% | 76.92% | 55.56% |
| loan_agreement_in_040 | loan_agreement | 7 | 13 | 3 | 35.00% | 70.00% | 46.67% |
| loan_agreement_in_041 | loan_agreement | 11 | 9 | 2 | 55.00% | 84.62% | 66.67% |
| loan_agreement_in_042 | loan_agreement | 7 | 11 | 3 | 38.89% | 70.00% | 50.00% |
| loan_agreement_us_001 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_002 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_003 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_004 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_005 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_006 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_007 | loan_agreement | 11 | 8 | 1 | 57.89% | 91.67% | 70.97% |
| loan_agreement_us_008 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_009 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_010 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_011 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_012 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_013 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_014 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_015 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_016 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_017 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_018 | loan_agreement | 11 | 8 | 1 | 57.89% | 91.67% | 70.97% |
| loan_agreement_us_019 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_020 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_021 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_022 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_023 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_024 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_025 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_026 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_027 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_028 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_029 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_030 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_031 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_032 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_033 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_034 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_035 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_036 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_037 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_038 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_039 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_040 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| loan_agreement_us_041 | loan_agreement | 11 | 7 | 1 | 61.11% | 91.67% | 73.33% |
| loan_agreement_us_042 | loan_agreement | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| tax_form_in_001 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_002 | tax_form | 7 | 9 | 2 | 43.75% | 77.78% | 56.00% |
| tax_form_in_003 | tax_form | 7 | 9 | 2 | 43.75% | 77.78% | 56.00% |
| tax_form_in_004 | tax_form | 7 | 10 | 2 | 41.18% | 77.78% | 53.85% |
| tax_form_in_005 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_006 | tax_form | 7 | 11 | 2 | 38.89% | 77.78% | 51.85% |
| tax_form_in_007 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_008 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_009 | tax_form | 6 | 13 | 3 | 31.58% | 66.67% | 42.86% |
| tax_form_in_010 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_011 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_012 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_013 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_014 | tax_form | 7 | 9 | 2 | 43.75% | 77.78% | 56.00% |
| tax_form_in_015 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_016 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_017 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_018 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_019 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_020 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_021 | tax_form | 8 | 7 | 1 | 53.33% | 88.89% | 66.67% |
| tax_form_in_022 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_023 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_024 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_025 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_026 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_027 | tax_form | 5 | 13 | 4 | 27.78% | 55.56% | 37.04% |
| tax_form_in_028 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_029 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_030 | tax_form | 6 | 13 | 3 | 31.58% | 66.67% | 42.86% |
| tax_form_in_031 | tax_form | 6 | 13 | 3 | 31.58% | 66.67% | 42.86% |
| tax_form_in_032 | tax_form | 6 | 10 | 3 | 37.50% | 66.67% | 48.00% |
| tax_form_in_033 | tax_form | 7 | 11 | 2 | 38.89% | 77.78% | 51.85% |
| tax_form_in_034 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_035 | tax_form | 7 | 12 | 2 | 36.84% | 77.78% | 50.00% |
| tax_form_in_036 | tax_form | 7 | 9 | 2 | 43.75% | 77.78% | 56.00% |
| tax_form_in_037 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_038 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_in_039 | tax_form | 7 | 10 | 2 | 41.18% | 77.78% | 53.85% |
| tax_form_in_040 | tax_form | 5 | 12 | 4 | 29.41% | 55.56% | 38.46% |
| tax_form_in_041 | tax_form | 6 | 11 | 3 | 35.29% | 66.67% | 46.15% |
| tax_form_in_042 | tax_form | 6 | 12 | 3 | 33.33% | 66.67% | 44.44% |
| tax_form_us_001 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_002 | tax_form | 4 | 10 | 2 | 28.57% | 66.67% | 40.00% |
| tax_form_us_003 | tax_form | 4 | 10 | 2 | 28.57% | 66.67% | 40.00% |
| tax_form_us_004 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_005 | tax_form | 5 | 7 | 1 | 41.67% | 83.33% | 55.56% |
| tax_form_us_006 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_007 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_008 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_009 | tax_form | 4 | 10 | 2 | 28.57% | 66.67% | 40.00% |
| tax_form_us_010 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_011 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_012 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_013 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_014 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_015 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_016 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_017 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_018 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_019 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_020 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_021 | tax_form | 4 | 9 | 2 | 30.77% | 66.67% | 42.11% |
| tax_form_us_022 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_023 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_024 | tax_form | 4 | 10 | 2 | 28.57% | 66.67% | 40.00% |
| tax_form_us_025 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_026 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_027 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_028 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_029 | tax_form | 4 | 9 | 2 | 30.77% | 66.67% | 42.11% |
| tax_form_us_030 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_031 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_032 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_033 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_034 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_035 | tax_form | 4 | 9 | 2 | 30.77% | 66.67% | 42.11% |
| tax_form_us_036 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_037 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_038 | tax_form | 4 | 10 | 2 | 28.57% | 66.67% | 40.00% |
| tax_form_us_039 | tax_form | 4 | 9 | 2 | 30.77% | 66.67% | 42.11% |
| tax_form_us_040 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |
| tax_form_us_041 | tax_form | 5 | 8 | 1 | 38.46% | 83.33% | 52.63% |
| tax_form_us_042 | tax_form | 5 | 9 | 1 | 35.71% | 83.33% | 50.00% |

## Failure Analysis


### Missed PII (False Negatives) — 681 total

| Document | Type | Value | Position |
|----------|------|-------|----------|
| bank_statement_in_001 | ADDRESS | `33/02, Jain Path, Guna 560429` | 577-606 |
| bank_statement_in_002 | ADDRESS | `71/623, Buch Nagar, Mehsana 665605` | 574-608 |
| bank_statement_in_003 | ACCOUNT_NUMBER | `9179618942` | 380-390 |
| bank_statement_in_003 | ADDRESS | `08, Chandra Circle, Srikakulam-916585` | 577-614 |
| bank_statement_in_004 | ACCOUNT_NUMBER | `017113053606` | 380-392 |
| bank_statement_in_004 | ADDRESS | `90/922, Deshmukh Marg, Nangloi Jat 76636...` | 579-620 |
| bank_statement_in_005 | ACCOUNT_NUMBER | `9441190772` | 380-390 |
| bank_statement_in_005 | ADDRESS | `56/79, Gera Path, Latur 997345` | 575-605 |
| bank_statement_in_006 | ADDRESS | `08/38, Kara Chowk, Bhiwani-433680` | 583-616 |
| bank_statement_in_008 | ADDRESS | `H.No. 87, Khalsa Circle, Darbhanga-98124...` | 585-626 |
| bank_statement_in_009 | ADDRESS | `H.No. 919, Nair Circle, Berhampore 19310...` | 573-614 |
| bank_statement_in_010 | ADDRESS | `H.No. 563, Sundaram Road, Proddatur-7257...` | 574-616 |
| bank_statement_in_011 | ACCOUNT_NUMBER | `012699835448` | 370-382 |
| bank_statement_in_011 | ADDRESS | `72/362, Jha Road, Siwan-386300` | 570-600 |
| bank_statement_in_012 | ADDRESS | `20/99, Bajaj Marg, Madurai-780738` | 570-603 |
| bank_statement_in_013 | ADDRESS | `H.No. 055, Mitter Zila, Barasat-169041` | 580-618 |
| bank_statement_in_014 | ACCOUNT_NUMBER | `243090674453` | 387-399 |
| bank_statement_in_014 | ADDRESS | `H.No. 749, Edwin Path, Haldia 800520` | 585-621 |
| bank_statement_in_015 | ADDRESS | `20/221, Bahri Path, Nanded 552901` | 574-607 |
| bank_statement_in_016 | ADDRESS | `11, Mane Street, Berhampore-864313` | 579-613 |
| bank_statement_in_017 | ADDRESS | `51/015, Barad Road, Chittoor-920316` | 578-613 |
| bank_statement_in_019 | ACCOUNT_NUMBER | `0464659121422` | 377-390 |
| bank_statement_in_019 | ADDRESS | `H.No. 14, Mand Chowk, Kharagpur 102686` | 581-619 |
| bank_statement_in_020 | ADDRESS | `H.No. 72, Dhingra Chowk, Dewas-982562` | 571-608 |
| bank_statement_in_021 | ADDRESS | `10/001, Guha Road, Surat 728873` | 583-614 |
| bank_statement_in_022 | ACCOUNT_NUMBER | `5445495760` | 380-390 |
| bank_statement_in_022 | ADDRESS | `71/681, Deol Circle, Shimoga 663085` | 576-611 |
| bank_statement_in_023 | ADDRESS | `74, Bakshi Chowk, Chennai 768588` | 568-600 |
| bank_statement_in_024 | ADDRESS | `H.No. 302, Nigam Path, Kakinada 397813` | 584-622 |
| bank_statement_in_025 | ACCOUNT_NUMBER | `1967591666` | 382-392 |

*... and 651 more*


### False Detections (False Positives) — 4485 total

| Document | Type | Value | Position | Best IoU |
|----------|------|-------|----------|----------|
| bank_statement_in_001 | ADDRESS | `560429` | 600-606 | 0.21 |
| bank_statement_in_001 | ACCOUNT_NUMBER | `56622148` | 1621-1629 | 0.00 |
| bank_statement_in_001 | PERSON_NAME | `Jain Path, Guna` | 593-608 | 0.00 |
| bank_statement_in_001 | ADDRESS | `Mumbai` | 704-710 | 0.00 |
| bank_statement_in_001 | ORGANIZATION | `Bharath National Bank
FDIC Insured` | 2079-2113 | 0.00 |
| bank_statement_in_002 | ADDRESS | `665605` | 602-608 | 0.18 |
| bank_statement_in_002 | PERSON_NAME | `Rajagopalan` | 1258-1269 | 0.00 |
| bank_statement_in_002 | ACCOUNT_NUMBER | `60555188` | 1443-1451 | 0.00 |
| bank_statement_in_002 | PERSON_NAME | `Buch Nagar` | 598-608 | 0.00 |
| bank_statement_in_002 | PERSON_NAME | `Mehsana` | 610-617 | 0.00 |
| bank_statement_in_002 | ORGANIZATION | `Devi` | 2600-2604 | 0.00 |
| bank_statement_in_003 | PHONE | `9179618942` | 380-390 | 0.00 |
| bank_statement_in_003 | ADDRESS | `916585` | 608-614 | 0.16 |
| bank_statement_in_003 | ACCOUNT_NUMBER | `30605633` | 1723-1731 | 0.00 |
| bank_statement_in_003 | PERSON_NAME | `Chandra Circle` | 585-599 | 0.00 |
| bank_statement_in_004 | PHONE | `017113053606` | 380-392 | 0.00 |
| bank_statement_in_004 | ADDRESS | `766360` | 614-620 | 0.15 |
| bank_statement_in_004 | ACCOUNT_NUMBER | `39600029` | 1275-1283 | 0.00 |
| bank_statement_in_004 | ACCOUNT_NUMBER | `48777295` | 1827-1835 | 0.00 |
| bank_statement_in_004 | ORGANIZATION | `Peninsula Banking Corporation` | 81-110 | 0.00 |
| bank_statement_in_004 | PERSON_NAME | `Deshmukh Marg` | 591-604 | 0.00 |
| bank_statement_in_004 | PERSON_NAME | `Nangloi Jat` | 606-617 | 0.00 |
| bank_statement_in_004 | PHONE | `164.29` | 1898-1904 | 0.00 |
| bank_statement_in_004 | ORGANIZATION | `Peninsula Banking Corporation` | 2383-2412 | 0.00 |
| bank_statement_in_005 | PHONE | `9441190772` | 380-390 | 0.00 |
| bank_statement_in_005 | ADDRESS | `997345` | 599-605 | 0.20 |
| bank_statement_in_005 | PERSON_NAME | `Gera Path` | 588-597 | 0.00 |
| bank_statement_in_006 | ADDRESS | `433680` | 610-616 | 0.18 |
| bank_statement_in_006 | ACCOUNT_NUMBER | `82428292` | 1998-2006 | 0.00 |
| bank_statement_in_006 | PERSON_NAME | `Kara Chowk` | 598-608 | 0.00 |