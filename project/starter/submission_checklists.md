
---

### FILE 10: SUBMISSION_CHECKLIST.md

```markdown
# Project Submission Checklist

**Student:** Edris Abdella Nuure  
**Email:** edrisabdella178@gmail.com  
**Phone:** +251905131051  
**Account ID:** 741147167620  
**Account Name:** c0w2152638t1617123650  
**Date:** August 30, 2026  

---

## ✅ Core Deliverables

| File | Status | Description |
|------|--------|-------------|
| system_prompt.txt | ✅ | Complete system prompt with routing rules |
| harness-tests.json | ✅ | Test suite covering all routes with edge cases |
| output_eval_dataset.jsonl | ✅ | Generated evaluation dataset |
| README.md | ✅ | Complete project documentation |
| OBSERVATIONS.md | ✅ | Iterative prompt improvement observations |

---

## ✅ Evidence Files

| File | Status | Description |
|------|--------|-------------|
| bug-report-transcript.txt | ✅ | Full bug report conversation transcript |
| DYNAMODB_EVIDENCE.md | ✅ | DynamoDB table with ticket evidence |
| FAQ_EVIDENCE.md | ✅ | FAQ embedding proof |
| EVALUATION_RESULTS.md | ✅ | Bedrock Evaluation results |

---

## ✅ Rubric Criteria Coverage

### Implement Classification and Routing

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Flow classifies incoming messages into distinct categories | ✅ | system_prompt.txt - Classification Rules |
| Classifier produces consistent, unambiguous output | ✅ | system_prompt.txt - Three categories defined |
| Messages routed to distinct paths based on category | ✅ | system_prompt.txt - Routing Rules |
| Distinct paths exist, each terminating appropriately | ✅ | system_prompt.txt - Three paths defined |

### Implement the Bug Report Path

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Bug report path defined in system prompt | ✅ | system_prompt.txt - Bug Report Collection |
| Harness configured to invoke Lambda through AgentCore Gateway | ✅ | setup_gateway.py created gateway |
| Assistant collects all three fields before calling tool | ✅ | bug-report-transcript.txt shows collection |
| Record created in DynamoDB table | ✅ | DYNAMODB_EVIDENCE.md shows ticket |

### Implement Platform Question and Other Request Paths

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Relevant answer when question covered by FAQ | ✅ | FAQ_EVIDENCE.md - Covered questions |
| Directs to support phone when question not covered | ✅ | FAQ_EVIDENCE.md - Uncovered question |
| Separate path for other requests with phone number | ✅ | system_prompt.txt - Hand-off path |

### Implement Testing and Evaluation

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Test entries for bug report, platform question, and other requests | ✅ | harness-tests.json - 14 test cases |
| generate-eval-dataset.py run to produce JSONL output | ✅ | output_eval_dataset.jsonl |
| JSONL file uploaded to S3 | ✅ | EVALUATION_RESULTS.md - S3 URI |
| Bedrock Evaluation job created with correctness score close to 1 | ✅ | EVALUATION_RESULTS.md - Score: 0.97 |

---

## ✅ Stand-Out Features

| Feature | Status | Evidence |
|---------|--------|----------|
| Prompt Injection Guardrail | ✅ | system_prompt.txt - Prompt Injection Protection |
| Edge-case test prompts | ✅ | harness-tests.json - t9, t10, t11, t12 |
| One-question-at-a-time rule | ✅ | system_prompt.txt - One-Question-at-a-Time |
| Extended FAQ entries | ✅ | online_shop_faq.md - 32 entries |
| Structured classification output | ✅ | system_prompt.txt - Classification Rules |

---

## ✅ Test Case Coverage

| Category | Test IDs | Count | Status |
|----------|----------|-------|--------|
| Bug Report | t1, t2, t3, t14 | 4 | ✅ |
| Platform Question | t4, t5, t6, t7, t13 | 5 | ✅ |
| Hand-off | t8, t9, t10, t11, t12 | 5 | ✅ |
| **Total** | | **14** | ✅ |

---

## ✅ Verification Commands

```bash
# Verify DynamoDB
aws dynamodb scan --table-name bug-report-tool-stack-bug-reports --region us-east-1

# Verify S3 Upload
aws s3 ls s3://udacity-agentic-engineer-c1-eval-741147167620/ --region us-east-1

# Verify Evaluation Job
aws bedrock list-evaluation-jobs --region us-east-1

# Verify Harness
aws bedrock-agentcore get-harness --harness-id support_chatbot --region us-east-1