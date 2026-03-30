from fastapi import FastAPI, HTTPException
from app.models import (
    InquiryRequest,
    ClassificationResponse,
    EscalationRequest,
    EscalationResponse,
)
from app.classifier import classify_question
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

app = FastAPI(title="Capital Home Escalation Service")


def send_escalation_email(
    notify_email: str,
    customer_question: str,
    category: str,
    reason: str,
    customer_name: str | None = None,
    customer_contact: str | None = None,
) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM")

    if not all([smtp_host, smtp_port, smtp_username, smtp_password, smtp_from]):
        raise ValueError("SMTP environment variables are not fully configured.")

    subject = f"Customer Inquiry Escalation - {category}"

    body = f"""A customer inquiry could not be answered automatically and requires follow-up.

Customer question:
{customer_question}

Category:
{category}

Reason for escalation:
{reason}

Customer name:
{customer_name or 'Not provided'}

Customer contact:
{customer_contact or 'Not provided'}
"""

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_from
    msg["To"] = notify_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify", response_model=ClassificationResponse)
def classify(request: InquiryRequest):
    result = classify_question(request.customer_question)
    return ClassificationResponse(**result)


@app.post("/escalate", response_model=EscalationResponse)
def escalate(request: EscalationRequest):
    try:
        send_escalation_email(
            notify_email=request.notify_email,
            customer_question=request.customer_question,
            category=request.category,
            reason=request.reason,
            customer_name=request.customer_name,
            customer_contact=request.customer_contact,
        )
        return EscalationResponse(
            status="sent",
            message=f"Escalation email sent to {request.notify_email}.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to send escalation email: {exc}")