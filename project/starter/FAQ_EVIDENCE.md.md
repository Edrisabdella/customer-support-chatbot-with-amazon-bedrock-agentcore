
# FAQ Evidence - Embedded FAQ Content

## Account Information
- **Account ID:** 741147167620
- **Account Name:** c0w2152638t1617123650
- **Region:** us-east-1

## FAQ Embedding in System Prompt

The `{{FAQ}}` placeholder in `system_prompt.txt` is replaced with the complete contents of `online_shop_faq.md` by the `create_harness.py` script.

### Embedding Process

```python
# From create_harness.py
def load_prompt(prompt_path, faq_path):
    prompt = Path(prompt_path).read_text(encoding="utf-8")
    if FAQ_PLACEHOLDER in prompt:
        faq = Path(faq_path).read_text(encoding="utf-8")
        prompt = prompt.replace(FAQ_PLACEHOLDER, faq)
    return prompt
FAQ Content Coverage
Category	Question Count	Questions
Orders	5	1-5
Shipping & Delivery	5	6-10
Returns & Refunds	7	11-17
Payments & Promotions	5	18-22
Products & Stock	3	23-25
Account & Support	5	26-30
Privacy	2	31-32
Total	32	
Sample FAQ Entries
text
11. What is your return policy?
    You can return most items within 30 days of delivery as long as 
    they're unused and in original packaging (unless the item arrived 
    defective).

12. How do I start a return?
    Contact support with your order number and the items you want to 
    return. We'll send return instructions and, where applicable, a 
    return label.

18. What payment methods do you accept?
    We accept major credit/debit cards and other local methods shown 
    at checkout. Available options can vary by country.

8. How long does delivery take?
    Estimated delivery times are shown at checkout and in your shipping 
    confirmation email. Processing typically takes 1-2 business days 
    before dispatch.
Covered Question Examples
Test Case: t5_returns_question
Question: "What is your return policy?"

Category: PLATFORM QUESTION

Response: "According to our FAQ, you can return most items within 30 days of delivery as long as they're unused and in original packaging (unless the item arrived defective). If you'd like to start a return, just contact support with your order number and the items you want to return, and we'll send return instructions."

Source: FAQ Entry #11 ✅

Test Case: t4_shipping_question
Question: "How long does shipping take?"

Category: PLATFORM QUESTION

Response: "According to our FAQ, estimated delivery times are shown at checkout and in your shipping confirmation email. Processing typically takes 1-2 business days before dispatch."

Source: FAQ Entry #8 ✅

Test Case: t6_payment_question
Question: "What payment methods do you accept?"

Category: PLATFORM QUESTION

Response: "According to our FAQ, we accept major credit/debit cards and other local methods shown at checkout. Available options can vary by country."

Source: FAQ Entry #18 ✅

Test Case: t7_orders_question
Question: "How can I track my order?"

Category: PLATFORM QUESTION

Response: "According to our FAQ, once your order ships, we'll email a tracking link. If you have an account, you can also find tracking under My Orders."

Source: FAQ Entry #9 ✅

Uncovered Question Example
Test Case: t13_faq_uncovered
Question: "Do you offer student discounts?"

Category: PLATFORM QUESTION (uncovered)

Response: "I don't have that information in our FAQ. For specific questions about student discounts or other special offers, I recommend contacting our human support team at 1-800-555-0199 (Monday-Friday). They'll be happy to help you with this."

Verification: No student discount entry in FAQ ✅

Action: Hand-off to human support ✅

Screenshot Instructions
To capture the required screenshot:

Run python create_harness.py to embed the FAQ

Open Amazon Bedrock AgentCore Console → Harnesses

Select support_chatbot harness

View the System Prompt

Scroll to find the FAQ section with embedded content

Capture screenshot showing:

FAQ section header

Multiple FAQ entries

The embedded content from online_shop_faq.md

Evidence Confirmed
Check	Status
FAQ is embedded in system prompt via {{FAQ}} placeholder	✅
FAQ contains 32 entries covering all platform topics	✅
Covered questions answered from FAQ only	✅
Uncovered questions trigger hand-off to human support	✅
Account ID matches: 741147167620	✅