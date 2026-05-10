"""Appointment models with AI no-show prediction."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class AppointmentCreate(BaseModel):
    patient_id: str
    patient_phone: str
    branch_id: str = Field(..., description="jeddah-main, jeddah-north, etc.")
    department: str = Field(..., description="medical-spa, optometry, dermatology, etc.")
    doctor_id: Optional[str] = None
    scheduled_time: datetime
    reason: Optional[str] = None
    insurance_national_id: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: str
    patient_id: str
    scheduled_time: datetime
    branch_id: str
    department: str
    doctor_id: Optional[str] = None
    status: str  # confirmed, checked-in, completed, no-show, cancelled
    no_show_risk: float = Field(0.0, ge=0.0, le=1.0)
    created_at: datetime
    reminded_24h: bool = False
    reminded_2h: bool = False
