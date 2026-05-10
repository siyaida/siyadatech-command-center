"""SQLAlchemy models for Ragaban Clinics — PDPL-compliant design."""
from sqlalchemy import Column, String, DateTime, Float, Boolean, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db import Base
import uuid
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    national_id = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(255), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)
    branch_preference = Column(String(50), default="jeddah-main")
    
    # PDPL compliance
    consent_marketing = Column(Boolean, default=False)
    consent_data_processing = Column(Boolean, default=True)
    data_retention_expiry = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    payments = relationship("Payment", back_populates="patient")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    branch_id = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    doctor_id = Column(String(50), nullable=True)
    scheduled_time = Column(DateTime, nullable=False)
    reason = Column(Text, nullable=True)
    
    status = Column(String(20), default="confirmed")  # confirmed, checked-in, completed, no-show, cancelled
    no_show_risk = Column(Float, default=0.0)
    
    # Reminder tracking
    reminded_24h = Column(Boolean, default=False)
    reminded_2h = Column(Boolean, default=False)
    reminder_whatsapp_id = Column(String(100), nullable=True)
    
    # Insurance
    insurance_national_id = Column(String(10), nullable=True)
    claim_id = Column(String(100), nullable=True)
    claim_status = Column(String(20), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="appointments")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"), nullable=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="SAR")
    method = Column(String(20), nullable=False)  # mada, visa, mastercard, applepay, stcpay, cash
    status = Column(String(20), default="created")  # created, pending, completed, failed, refunded
    
    # Geidea tracking
    geidea_payment_id = Column(String(100), nullable=True)
    geidea_checkout_url = Column(Text, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    description = Column(String(255), default="Ragaban Clinic Services")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="payments")

class ClinicBranch(Base):
    __tablename__ = "clinic_branches"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100), nullable=True)
    address = Column(Text, nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(255), nullable=True)
    
    # Operating hours
    opening_time = Column(String(5), default="09:00")
    closing_time = Column(String(5), default="21:00")
    
    # Services offered at this branch
    services = Column(JSONB, default=list)
    
    # Capacity
    max_daily_appointments = Column(Integer, default=100)
    current_appointment_count = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Integer
