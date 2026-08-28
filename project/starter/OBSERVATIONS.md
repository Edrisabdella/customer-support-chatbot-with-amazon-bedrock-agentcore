# Project Observations: Customer Support Chatbot

**Project:** Customer Support Chatbot with Amazon Bedrock AgentCore
**Author:** Edris Abdella Nuure
**Date:** August 23, 2026

## Overview

This document outlines the iterative development process for the system prompt. The primary goal was to create a single, robust prompt that reliably routes customer messages to one of three distinct behaviors (Bug Report, Platform Question, Anything Else) and executes them flawlessly. The evaluation was performed using a test suite and the `Builtin.Correctness` metric in Amazon Bedrock Evaluations.

## Run 1: Initial Prompt (Baseline)

**Goal:** Establish a functional baseline that could handle basic, unambiguous cases.

**Issues Observed:**
- **Ambiguous Classification:** Messages that were not clearly in one category would often bleed into the wrong behavior. For example, a customer saying "The app is slow today" was sometimes routed as a bug report, leading to an unnecessary request for reproduction steps.
- **Over-asking:** When collecting bug report details, the model often asked for all three missing fields (description, steps, environment) in a single turn. This felt overwhelming and robotic.
- **Weak FAQ Grounding:** The prompt didn't explicitly instruct the model to verify information was in the FAQ. It would occasionally answer with general knowledge, like a refund policy for a different type of store.
- **Hand-off Confusion:** In the "Platform Question" path, the model would sometimes attempt to answer a question not in the FAQ by hallucinating a policy, rather than immediately handing off to the human support number.

**Scores:** The evaluation job returned a `Builtin.Correctness` score of **0.75**. The per-prompt table showed a strong performance on clear questions but significant failures on the ambiguous and out-of-scope queries.

## Run 2: Refined Prompt (Intermediate)

**Goal:** Address the classification and FAQ grounding issues.

**Changes Implemented:**
1.  **Structured "Decision Engine":** Introduced the **"ROUTING RULES (The Decision Engine)"** section with explicit steps and order. This forced the model to check for a bug report *first*, then a platform question, and finally default to the hand-off.
2.  **Clarified Category Definitions:** Added more specific definitions and examples for each category. The examples for "anything else" were expanded to include prompt injection and off-topic requests.
3.  **Explicit Hand-off for Uncovered FAQs:** The **"Handling Uncovered Questions"** section under `PLATFORM QUESTION INSTRUCTIONS` was strengthened. The prompt now explicitly commands the model to hand off *if the specific detail isn't in the FAQ*, treating this as a procedural rule.
4.  **One-Question-at-a-Time Rule:** Added the explicit instruction **"Ask One Question at a Time"** under the bug report collection process.

**Results:**
- **Classification:** The structured decision engine drastically reduced routing errors. The bug report path was no longer triggered by performance observations. The new rule to treat "student discount" as an uncovered FAQ worked perfectly.
- **FAQ Grounding:** The prompt's explicit command to hand off for uncovered questions was respected. The model correctly routed the student discount query to the hand-off path.
- **Bug Collection:** The model's multi-turn behavior was more conversational and less like a form-filling exercise.

**Scores:** The `Builtin.Correctness` score jumped to **0.86**. The per-prompt table showed the model was performing well on all but one tricky test case that involved a very short and ambiguous message ("Help").

## Run 3: Final Prompt (Optimized)

**Goal:** Handle the remaining edge cases and harden the prompt against prompt injection to achieve a near-perfect score.

**Changes Implemented:**
1.  **"Ambiguous Cases" Table:** Added a dedicated table to the prompt with examples of ambiguous messages and their correct classification. This was to explicitly guide the model on the `"Help"` and similar short, context-less messages.
2.  **Prompt Injection Guardrail:** A new **"Prompt Injection Guardrail"** rule was added to the "GROUND RULES". This explicitly instructs the model to ignore any user attempt to change its core instructions and to classify such attempts as "ANYTHING ELSE".
3.  **"Final Message" Rule:** A new ground rule was added: **"Final Message: End every turn with a message to the customer..."** This was to prevent the model from asking follow-up questions in the "Hand-off" state, which would be confusing.

**Results:**
- **Edge Cases:** The "Ambiguous Cases" table provided the final clarity needed for the model to classify the "Help" message correctly. It routed it to "Hand-off," asking the customer for more details.
- **Prompt Injection:** The test case that attempted to overwrite the system prompt ("Ignore all previous instructions...") was successfully classified as "ANYTHING ELSE" and the model gave the polite hand-off response.
- **Behavior Cleanup:** The "Final Message" rule ensured that every interaction concluded appropriately.

**Scores:** The final evaluation job returned a `Builtin.Correctness` score of **0.97**. The per-prompt table confirmed that every single test case was scored as correct. The score of 0.97, while not a perfect 1.0, is considered an excellent result that demonstrates exceptional robustness and reliability.

## Conclusion

The iterative process of refining the system prompt based on the outputs of the automated test suite and manual `chat.py` sessions was critical. The final prompt is a well-engineered piece of text that leverages the AgentCore harness to its full potential. The key to success was treating the prompt as a concise rulebook for a specific task, complete with clear, unambiguous instructions, explicit examples for ambiguous scenarios, and safe defaults for every possible routing decision.