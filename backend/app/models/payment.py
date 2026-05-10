"""Payment models for Geidea integration."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PaymentCreate(BaseModel):
    patient_id: str
    appointment_id: Optional[str] = None
    amount: float = Field(..., gt=0, description="Amount in SAR")
    method: str = Field(..., pattern=r"^(mada|visa|mastercard|applepay|stcpay)$")
    description: str = "Ragaban Clinic Services"
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str
    patient_id: str
    amount: float
    currency: str = "SAR"
    status: str  # created, pending, completed, failed, refunded
    checkout_url: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
