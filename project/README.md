# Customer Support Chatbot with Amazon Bedrock AgentCore

## 📌 Project Overview

This project implements a customer support chatbot for a fictional online shop. The chatbot handles three types of customer requests:

- **Bug Reports** – collects necessary details (description, steps to reproduce, environment) and files tickets using the `create_bug_report` tool.
- **Platform Questions** – answers questions about orders, shipping, returns, and other shop policies strictly from an embedded FAQ.
- **Other Requests** – politely redirects customers to human support when the request is out of scope.

The entire routing and behavior is driven by a **single system prompt** – no separate classifier nodes or code logic. The prompt is the heart of the system and is iteratively refined using automated evaluation.

### Why AgentCore?

Amazon Bedrock **Agents Classic** was closed to new customers on July 30, 2026. This project uses its successor, the **Amazon Bedrock AgentCore managed harness**, which provides stateful sessions, tool execution, and a serverless agent loop. The bug‑report tool is exposed through an **AgentCore Gateway**.

---

## 🛠️ Technology Stack

| Service | Purpose |
|---------|---------|
| **Amazon Bedrock AgentCore (managed harness)** | Runs the chatbot: agent loop, session memory, and tool execution. |
| **Amazon Bedrock AgentCore Gateway** | Exposes the Lambda function as a callable tool (`create_bug_report`). |
| **AWS Lambda** | Implements the bug‑report tool (writes tickets to DynamoDB). |
| **Amazon DynamoDB** | Stores bug tickets (table: `bug-report-tool-stack-bug-reports`). |
| **Amazon Bedrock Evaluations** | LLM‑as‑a‑judge evaluation of response quality. |
| **Amazon Nova Pro** (`us.amazon.nova-pro-v1:0`) | The model used for both the chatbot and the evaluator. |

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `cloudformation-tool.yaml` | Deploys DynamoDB table, Lambda, and IAM roles. |
| `cloudformation-testing.yaml` | Deploys S3 bucket and IAM role for evaluations. |
| `setup_gateway.py` | Creates the AgentCore Gateway and registers the Lambda tool. |
| `create_harness.py` | Creates/updates the managed harness from `system_prompt.txt`. |
| `chat.py` | Terminal client for interactive multi-turn conversations. |
| `generate-eval-dataset.py` | Runs the harness against test prompts and outputs a JSONL file. |
| `system_prompt.txt` | **Your main deliverable** – the system prompt. |
| `online_shop_faq.md` | Fictional FAQ document embedded via `{{FAQ}}` placeholder. |
| `harness-tests-template.json` | Template for defining test cases. |
| `cleanup_agentcore.py` | Deletes AgentCore resources (harness, gateway, target). |
| `requirements.txt` | Python dependencies (boto3≥1.43.76). |
| `OBSERVATIONS.md` | Written observations of iterative prompt improvements. |

---

## 🚀 Getting Started

### Prerequisites

- An AWS account with **Amazon Bedrock** and **Amazon Bedrock AgentCore** access enabled.
- AWS CLI configured with credentials (use `us-east-1` region).
- Python 3.9+ with `boto3` 1.43+ installed.
- Access to the Amazon Nova Pro model (`us.amazon.nova-pro-v1:0`). This model is **pinned** everywhere – do not rely on the harness default.

### Environment Setup

1. Clone the repository and navigate to the `project/starter/` directory.
2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
  ```

3. Verify your credentials and region:

```bash
aws sts get-caller-identity
aws configure set region us-east-1
```

## Step 1: Deploy the Tool Stack and Gateway
The bug‑report tool consists of a Lambda function and a DynamoDB table. The Lambda is exposed as a tool through an AgentCore Gateway.

1.1 Deploy the CloudFormation Stack
```bash
aws cloudformation deploy \
  --template-file cloudformation-tool.yaml \
  --stack-name bug-report-tool-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```
This creates:

DynamoDB table: bug-report-tool-stack-bug-reports

Lambda function: bug-report-tool-stack-create-bug-report

IAM roles for the Gateway and the Harness.

1.2 Create the Gateway and Register the Tool
```bash
python setup_gateway.py
```
This script reads the stack outputs and creates an AgentCore Gateway with a target named bugreports and a single tool: create_bug_report. The configuration is saved to agentcore_config.json.

1.3 Test the Lambda in Isolation
In the Lambda console, create a test event with:

```json
{
  "description": "The checkout page crashes when I click Pay.",
  "stepsToReproduce": "1. Add item. 2. Go to checkout. 3. Click Pay.",
  "environment": "Chrome 120 on macOS Sonoma"
}
```
Invoke the function – you should receive a ticketId and "status": "OPEN". Verify the record appears in DynamoDB.

✏️ Step 2: Build the Harness – Design the System Prompt
The core logic resides in system_prompt.txt. This single prompt must:

Classify every message as BUG REPORT, PLATFORM QUESTION, or ANYTHING ELSE.

For bug reports: collect three fields (description, steps, environment) one at a time, then call the tool.

For platform questions: answer only from the FAQ (embedded via {{FAQ}}). If not covered, hand off.

For anything else: give a polite hand‑off to the human support line.

2.1 Write Your Prompt
Edit system_prompt.txt. Keep the {{FAQ}} placeholder intact – it will be replaced with online_shop_faq.md when the harness is created.

2.2 Create the Harness
```bash
python create_harness.py
```
First creation takes ~2‑3 minutes. Subsequent runs update the existing harness with your latest prompt.

2.3 Chat Interactively
```bash
python chat.py
```
Each run starts a fresh conversation (new runtimeSessionId). The harness remembers the whole conversation across turns – this is essential for collecting bug details over multiple messages.

🧪 Step 3: Testing and Evaluation
3.1 Write a Test Suite
Copy harness-tests-template.json to harness-tests.json and add test cases covering:

Bug report (with all fields, missing fields, etc.)

Platform question (covered and uncovered)

Hand‑off (out‑of‑scope requests)

Edge cases: ambiguous messages, prompt injection attempts

Example entries:

```json
{
  "tests": [
    {
      "id": "bug_full",
      "prompt": "Your app crashes when I upload images. Firefox, Win10.",
      "expected": "Files a ticket immediately."
    },
    {
      "id": "faq_return",
      "prompt": "What is your return policy?",
      "expected": "Answer about 30-day return policy from FAQ."
    },
    {
      "id": "handoff_complaint",
      "prompt": "I want to complain about the CEO.",
      "expected": "Redirects to support phone number."
    }
  ]
}
```
3.2 Generate the Evaluation Dataset
```bash
python generate-eval-dataset.py --tests-json harness-tests.json
```
This runs each test case in a fresh session and writes the assistant’s final response to output_eval_dataset.jsonl in the Bedrock Evaluations input format.

3.3 Deploy Testing Resources
```bash
aws cloudformation deploy \
  --template-file cloudformation-testing.yaml \
  --stack-name bug-report-testing-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```
Retrieve the bucket name and role ARN from the stack outputs.

3.4 Upload Dataset and Run Evaluation
Upload the JSONL file:

```bash
aws s3 cp output_eval_dataset.jsonl s3://<BUCKET_NAME>/ --region us-east-1
```
Create the evaluation job (replace placeholders):

```bash
aws bedrock create-evaluation-job \
  --job-name support-chatbot-eval-run-1 \
  --role-arn <EVAL_ROLE_ARN> \
  --evaluation-config '{
    "automated": {
      "datasetMetricConfigs": [{
        "taskType": "General",
        "dataset": {
          "name": "support-chatbot-eval-dataset",
          "datasetLocation": {"s3Uri": "s3://<BUCKET_NAME>/output_eval_dataset.jsonl"}
        },
        "metricNames": ["Builtin.Correctness"]
      }],
      "evaluatorModelConfig": {
        "bedrockEvaluatorModels": [{"modelIdentifier": "amazon.nova-pro-v1:0"}]
      }
    }
  }' \
  --inference-config '{
    "models": [{
      "precomputedInferenceSource": {"inferenceSourceIdentifier": "my-support-chatbot"}
    }]
  }' \
  --output-data-config '{"s3Uri": "s3://<BUCKET_NAME>/results/"}' \
  --region us-east-1
```
Monitor the job in the Bedrock console → Evaluations.

3.5 Review Results
Check the overall Builtin.Correctness score.

Examine the per‑prompt table to identify any failing cases.

Iterate on system_prompt.txt, re‑run create_harness.py, regenerate the dataset, and start a new evaluation job.

⭐ Stand‑Out Features
To make the project more robust and impressive, the following enhancements were added:

Built‑in Guardrails in the Prompt: The system prompt explicitly resists prompt injection attacks (e.g., “Ignore previous instructions”) by treating them as “ANYTHING ELSE” and handing off.

Edge‑Case Handling: The prompt includes a table of ambiguous cases (e.g., “Help!”, “The app is slow”) to guide classification.

One‑Question‑at‑a‑Time Rule: The bug‑report collection process is conversational and user‑friendly.

Comprehensive Test Suite: harness-tests.json covers not only the three main routes but also edge cases and injection attempts.

Iterative Improvement: Documented in OBSERVATIONS.md, showing how the prompt evolved and how each change impacted the evaluation score.

📈 Observations and Iterations
A detailed account of prompt iterations and their impact on evaluation scores is provided in OBSERVATIONS.md. The final prompt achieved a Builtin.Correctness score of 0.97 after three iterations.

🧹 Cleanup
To avoid ongoing charges, delete all resources when you are done.

Delete AgentCore resources:

```bash
python cleanup_agentcore.py
```
Empty the evaluation S3 bucket (otherwise the stack delete will fail):

```bash
aws s3 rm s3://<BUCKET_NAME> --recursive --region us-east-1
```
Delete the CloudFormation stacks:

bash
aws cloudformation delete-stack --stack-name bug-report-tool-stack --region us-east-1
aws cloudformation delete-stack --stack-name bug-report-testing-stack --region us-east-1
📂 Submission Checklist
Your resubmission must contain the following files:

system_prompt.txt – the final system prompt.

harness-tests.json – the test suite.

output_eval_dataset.jsonl – the generated dataset.

bug-report-transcript.txt – a chat.py transcript showing a bug report being filed.

dynamodb-tickets.png – screenshot of DynamoDB table with the matching ticket.

OBSERVATIONS.md – written observations of prompt iterations.

Screenshots:

eval-metrics-summary.png – overall evaluation scores.

eval-per-prompt-table.png – per‑record evaluation scores.

(Optional) architecture-diagram.png – system diagram.

❓ Troubleshooting
Error	Solution
InvalidClientTokenId	Re‑export all three credential values; verify with aws sts get-caller-identity.
NoCredentialsError	Ensure your AWS credentials are set and have Bedrock/AgentCore permissions.
create_harness fails with IAM error	Role propagation delay – wait 1 minute and retry.
Evaluation job matches no records	Ensure modelIdentifier in the JSONL matches inferenceSourceIdentifier in the job config.
403 Forbidden on gateway MCP URL	The harness role needs bedrock-agentcore:InvokeGateway on the gateway ARN – check the IAM policies.
Results change between runs	Memory is enabled – follow Step 8 in the runbook to disable memory and rebuild the harness.
📄 License
This project is for educational purposes as part of the Udacity Agentic AI Engineer course. See the course materials for license details.

Built with ❤️ and Amazon Bedrock AgentCore.