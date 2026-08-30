# Customer Support Chatbot with Amazon Bedrock AgentCore

**Student:** Edris Abdella Nuure  
**Email:** edrisabdella178@gmail.com  
**Account ID:** 741147167620  
**Date:** August 30, 2026  

---

## Project Overview

This project implements a customer support chatbot using the **Amazon Bedrock AgentCore managed harness**. The chatbot handles three types of customer requests:

1. **Bug Reports** – Collects bug description, steps to reproduce, and environment information, then files tickets using the `create_bug_report` tool.

2. **Platform Questions** – Answers questions about orders, shipping, returns, and payments using an embedded FAQ.

3. **Other Requests** – Politely redirects customers to human support when the request is out of scope.

The entire routing and behavior is driven by a **single system prompt** – no separate classifier nodes or code logic.

---

## Technology Stack

| Service | Purpose |
|---------|---------|
| Amazon Bedrock AgentCore (managed harness) | Runs the chatbot: agent loop, session memory, tool execution |
| Amazon Bedrock AgentCore Gateway | Exposes Lambda as `create_bug_report` tool |
| AWS Lambda | Bug report tool implementation |
| Amazon DynamoDB | Bug report storage |
| Amazon Bedrock Evaluations | LLM-as-a-judge evaluation |
| Amazon Nova Pro (us.amazon.nova-pro-v1:0) | Model for chatbot and evaluator |

---

## Project Files

| File | Description |
|------|-------------|
| system_prompt.txt | Main deliverable – system prompt with routing rules |
| harness-tests.json | Test suite covering all routes with edge cases |
| output_eval_dataset.jsonl | Generated evaluation dataset |
| bug-report-transcript.txt | Bug report conversation transcript |
| DYNAMODB_EVIDENCE.md | DynamoDB table evidence |
| FAQ_EVIDENCE.md | FAQ embedding evidence |
| EVALUATION_RESULTS.md | Bedrock Evaluation results |
| OBSERVATIONS.md | Iterative prompt improvement observations |
| README.md | Complete project documentation |

---

## Setup Instructions

### 1. Deploy Tool Stack

```bash
aws cloudformation deploy \
    --template-file cloudformation-tool.yaml \
    --stack-name bug-report-tool-stack \
    --capabilities CAPABILITY_NAMED_IAM \
    --region us-east-1