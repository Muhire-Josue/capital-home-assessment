ESCALATION_RESPONSE = (
    "I’m sorry, but I can’t confirm that automatically. "
    "I will escalate your inquiry to a team member for follow-up."
)


def classify_question(question: str) -> dict:
    q = question.lower().strip()

    pricing_keywords = ["price", "cost", "how much", "quote", "pricing"]
    stock_keywords = ["in stock", "available now", "availability", "do you have", "stock"]
    insurance_keywords = ["insurance", "covered", "coverage", "funding", "reimbursement"]
    delivery_keywords = ["deliver to", "delivery today", "delivery tomorrow", "ship to", "my address"]
    order_keywords = ["order status", "my order", "return", "refund", "exchange"]

    if any(k in q for k in pricing_keywords):
        return {
            "category": "pricing",
            "should_escalate": True,
            "response_message": ESCALATION_RESPONSE,
            "reason": "Exact pricing requires human confirmation.",
        }

    if any(k in q for k in stock_keywords):
        return {
            "category": "availability",
            "should_escalate": True,
            "response_message": ESCALATION_RESPONSE,
            "reason": "Live inventory requires human confirmation.",
        }

    if any(k in q for k in insurance_keywords):
        return {
            "category": "insurance_or_funding",
            "should_escalate": True,
            "response_message": ESCALATION_RESPONSE,
            "reason": "Coverage and funding questions require human confirmation.",
        }

    if any(k in q for k in delivery_keywords):
        return {
            "category": "delivery",
            "should_escalate": True,
            "response_message": ESCALATION_RESPONSE,
            "reason": "Specific delivery questions require human confirmation.",
        }

    if any(k in q for k in order_keywords):
        return {
            "category": "order_support",
            "should_escalate": True,
            "response_message": ESCALATION_RESPONSE,
            "reason": "Order-specific support requires human follow-up.",
        }

    return {
        "category": "general_faq",
        "should_escalate": False,
        "response_message": "This question can be handled by the FAQ chatbot.",
        "reason": "No escalation keyword matched.",
    }