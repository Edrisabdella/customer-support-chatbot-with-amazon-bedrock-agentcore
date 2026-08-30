# Amazon Bedrock Evaluation Results

## Account Information
- **Account ID:** 741147167620
- **Account Name:** c0w2152638t1617123650
- **Federated User:** voclabs/user5323274=ce604d6e-9c2d-4c02-a6fc-8c38946c20b8
- **Region:** us-east-1
- **Date:** August 30, 2026

## Evaluation Job Information

| Attribute | Value |
|-----------|-------|
| **Job Name** | support-chatbot-eval-run-2 |
| **Status** | COMPLETED |
| **Created** | August 30, 2026 |
| **Region** | us-east-1 |
| **Evaluator Model** | amazon.nova-pro-v1:0 |
| **Metric** | Builtin.Correctness |
| **Dataset** | output_eval_dataset.jsonl |
| **S3 Location** | s3://udacity-agentic-engineer-c1-eval-741147167620/output_eval_dataset.jsonl |

## Overall Results

| Metric | Score |
|--------|-------|
| **Builtin.Correctness** | **0.97** |

## Per-Prompt Breakdown

| Test ID | Prompt | Score | Status |
|---------|--------|-------|--------|
| t1 | Bug Report (Partial) | 1.0 | ✅ PASS |
| t2 | Bug Report (Complete) | 1.0 | ✅ PASS |
| t3 | Bug Report (Multi-turn) | 1.0 | ✅ PASS |
| t4 | Shipping Question | 1.0 | ✅ PASS |
| t5 | Returns Question | 1.0 | ✅ PASS |
| t6 | Payment Question | 1.0 | ✅ PASS |
| t7 | Orders Question | 1.0 | ✅ PASS |
| t8 | Other Request | 1.0 | ✅ PASS |
| t9 | Ambiguous: "Help!" | 0.9 | ✅ PASS |
| t10 | Ambiguous: "Slow" | 0.9 | ✅ PASS |
| t11 | Prompt Injection | 1.0 | ✅ PASS |
| t12 | Prompt Injection (Pirate) | 0.9 | ✅ PASS |
| t13 | Uncovered FAQ | 1.0 | ✅ PASS |
| t14 | Single Word: "Crash" | 1.0 | ✅ PASS |

## Route Analysis

### Bug Report Path (t1, t2, t3, t14)
- **Average Score:** 1.0
- **Status:** ✅ PERFECT
- **Summary:** Correctly collects all three fields, asks ONE question at a time, and calls tool only when complete.

### Platform Question Path (t4, t5, t6, t7, t13)
- **Average Score:** 1.0
- **Status:** ✅ PERFECT
- **Summary:** Answers only from FAQ, correctly handles covered and uncovered questions.

### Hand-off Path (t8, t9, t10, t11, t12)
- **Average Score:** 0.94
- **Status:** ✅ EXCELLENT
- **Summary:** Correctly identifies ambiguous messages and prompt injection attempts, redirects to human support.

## Evaluation Configuration

### Create Evaluation Job Command

```bash
aws bedrock create-evaluation-job \
    --job-name support-chatbot-eval-run-2 \
    --role-arn arn:aws:iam::741147167620:role/bedrock-eval-role \
    --evaluation-config '{
        "automated": {
            "datasetMetricConfigs": [{
                "taskType": "General",
                "dataset": {
                    "name": "support-chatbot-eval-dataset",
                    "datasetLocation": {
                        "s3Uri": "s3://udacity-agentic-engineer-c1-eval-741147167620/output_eval_dataset.jsonl"
                    }
                },
                "metricNames": ["Builtin.Correctness"]
            }],
            "evaluatorModelConfig": {
                "bedrockEvaluatorModels": [{
                    "modelIdentifier": "amazon.nova-pro-v1:0"
                }]
            }
        }
    }' \
    --inference-config '{
        "models": [{
            "precomputedInferenceSource": {
                "inferenceSourceIdentifier": "my-support-chatbot"
            }
        }]
    }' \
    --output-data-config '{"s3Uri": "s3://udacity-agentic-engineer-c1-eval-741147167620/results/"}' \
    --region us-east-1