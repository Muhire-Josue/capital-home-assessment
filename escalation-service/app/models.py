from pydantic import BaseModel, EmailStr
from typing import Optional


class InquiryRequest(BaseModel):
    customer_question: str
    customer_name: Optional[str] = None
    customer_contact: Optional[str] = None


class ClassificationResponse(BaseModel):
    category: str
    should_escalate: bool
    response_message: str
    reason: str


class EscalationRequest(BaseModel):
    customer_question: str
    category: str
    reason: str
    customer_name: Optional[str] = None
    customer_contact: Optional[str] = None
    notify_email: EmailStr


class EscalationResponse(BaseModel):
    status: str
    message: str