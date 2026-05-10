"""Pydantic models for patient data — PDPL-compliant field naming."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PatientCreate(BaseModel):
    """Patient registration — minimal PII, KSA format."""
    national_id: str = Field(..., pattern=r"^\d{10}$", description="Saudi national ID")
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., pattern=r"^\+9665\d{8}$", description="KSA mobile format")
    email: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = Field(None, pattern=r"^(male|female)$")
    branch_preference: Optional[str] = "jeddah-main"

class PatientResponse(BaseModel):
    id: str
    national_id: str
    name: str
    phone: str
    email: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
