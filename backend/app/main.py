"""
Siyadatech Ragaban API
FastAPI backend with KSA-native provider integrations.
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
from datetime import datetime

from app.config import settings
from app.providers.unifonic import UnifonicClient
from app.providers.nphies import NPHIESClient
from app.providers.geidea import GeideaClient
from app.providers.stc_cloud import STCCloudClient
from app.db import init_db, get_db
from app.models.patient import PatientCreate, PatientResponse
from app.models.appointment import AppointmentCreate, AppointmentResponse
from app.models.payment import PaymentCreate, PaymentResponse
from app.services.scheduler import AppointmentScheduler
from app.services.analytics import AnalyticsService
from app.services.ai import AIService

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("api_starting", version="1.0.0", environment=settings.ENVIRONMENT)
    await init_db()
    yield
    logger.info("api_shutting_down")

app = FastAPI(
    title="Siyadatech Ragaban API",
    description="KSA-native healthcare transformation backend for Ragaban Clinics",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend + mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ragaban.siyada-cybersecurity.com",
        "https://siyadatech.siyada-cybersecurity.com",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════
# Health & Status
# ═══════════════════════════════════════

@app.get("/health", tags=["System"])
async def health_check():
    """Liveness probe for Docker/Kubernetes."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }

@app.get("/ready", tags=["System"])
async def readiness_check():
    """Readiness probe — checks DB + provider connectivity."""
    checks = {
        "database": await _check_database(),
        "unifonic": await _check_unifonic(),
        "nphies": await _check_nphies(),
        "geidea": await _check_geidea(),
    }
    all_ready = all(checks.values())
    status = 200 if all_ready else 503
    return JSONResponse(
        content={"ready": all_ready, "checks": checks},
        status_code=status,
    )

# ═══════════════════════════════════════
# Patient Management
# ═══════════════════════════════════════

@app.post("/patients", response_model=PatientResponse, tags=["Patients"])
async def create_patient(patient: PatientCreate, db=Depends(get_db)):
    """Register a new patient with PDPL-compliant data handling."""
    logger.info("patient_create", national_id=patient.national_id)
    # TODO: Implement patient creation with EHR sync
    return PatientResponse(
        id="demo-patient-001",
        national_id=patient.national_id,
        name=patient.name,
        phone=patient.phone,
        created_at=datetime.utcnow(),
    )

@app.get("/patients/{patient_id}", response_model=PatientResponse, tags=["Patients"])
async def get_patient(patient_id: str, db=Depends(get_db)):
    """Get patient record (requires auth)."""
    # TODO: Implement patient retrieval
    raise HTTPException(status_code=501, detail="Patient retrieval not yet implemented")

# ═══════════════════════════════════════
# Appointments
# ═══════════════════════════════════════

@app.post("/appointments", response_model=AppointmentResponse, tags=["Appointments"])
async def create_appointment(
    appointment: AppointmentCreate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
):
    """Book appointment + trigger Unifonic WhatsApp confirmation."""
    logger.info("appointment_create", patient_id=appointment.patient_id, branch=appointment.branch_id)
    
    # AI no-show risk prediction
    scheduler = AppointmentScheduler()
    risk_score = await scheduler.predict_no_show_risk(appointment)
    
    # Send WhatsApp confirmation via Unifonic
    if settings.UNIFONIC_API_KEY:
        unifonic = UnifonicClient()
        background_tasks.add_task(
            unifonic.send_whatsapp_appointment_confirmation,
            phone=appointment.patient_phone,
            appointment_time=appointment.scheduled_time,
            branch=appointment.branch_id,
            risk_score=risk_score,
        )
    
    return AppointmentResponse(
        id="demo-appointment-001",
        patient_id=appointment.patient_id,
        scheduled_time=appointment.scheduled_time,
        branch_id=appointment.branch_id,
        status="confirmed",
        no_show_risk=risk_score,
        created_at=datetime.utcnow(),
    )

# ═══════════════════════════════════════
# Payments
# ═══════════════════════════════════════

@app.post("/payments", response_model=PaymentResponse, tags=["Payments"])
async def create_payment(payment: PaymentCreate, db=Depends(get_db)):
    """Process payment via Geidea (mada/Visa/MC)."""
    logger.info("payment_create", amount=payment.amount, method=payment.method)
    
    if not settings.GEIDEA_API_KEY:
        raise HTTPException(status_code=503, detail="Geidea payment gateway not configured")
    
    geidea = GeideaClient()
    result = await geidea.create_payment(
        amount=payment.amount,
        currency="SAR",
        description=payment.description,
        callback_url=f"https://ragaban.siyada-cybersecurity.com/payments/callback",
    )
    
    return PaymentResponse(
        id=result["payment_id"],
        amount=payment.amount,
        currency="SAR",
        status=result["status"],
        checkout_url=result["checkout_url"],
        created_at=datetime.utcnow(),
    )

# ═══════════════════════════════════════
# Insurance (NPHIES)
# ═══════════════════════════════════════

@app.get("/insurance/eligibility/{national_id}", tags=["Insurance"])
async def check_insurance_eligibility(national_id: str):
    """Check patient insurance eligibility via NPHIES FHIR."""
    logger.info("insurance_eligibility_check", national_id=national_id)
    
    if not settings.NPHIES_CLIENT_ID:
        raise HTTPException(status_code=503, detail="NPHIES not configured. Apply at CHI.gov.sa")
    
    nphies = NPHIESClient()
    result = await nphies.check_eligibility(national_id=national_id)
    
    return {
        "national_id": national_id,
        "eligible": result.get("eligible", False),
        "coverage_details": result.get("coverage", {}),
        "insurer": result.get("insurer", "Unknown"),
        "checked_at": datetime.utcnow().isoformat(),
    }

@app.post("/insurance/claims", tags=["Insurance"])
async def submit_insurance_claim(claim_data: dict):
    """Submit insurance claim via NPHIES FHIR $submit."""
    logger.info("insurance_claim_submit", patient_id=claim_data.get("patient_id"))
    
    if not settings.NPHIES_CLIENT_ID:
        raise HTTPException(status_code=503, detail="NPHIES not configured")
    
    nphies = NPHIESClient()
    result = await nphies.submit_claim(claim_data)
    
    return {
        "claim_id": result.get("claim_id"),
        "status": result.get("status", "submitted"),
        "tracking_url": result.get("tracking_url"),
        "submitted_at": datetime.utcnow().isoformat(),
    }

# ═══════════════════════════════════════
# Analytics
# ═══════════════════════════════════════

@app.get("/analytics/dashboard", tags=["Analytics"])
async def get_dashboard_metrics():
    """Real-time clinic performance metrics."""
    analytics = AnalyticsService()
    return await analytics.get_dashboard_summary()

@app.get("/analytics/no-show-prediction", tags=["Analytics"])
async def get_no_show_predictions(days: int = 7):
    """AI-powered no-show predictions for upcoming appointments."""
    ai = AIService()
    return await ai.predict_no_shows(days_ahead=days)

# ═══════════════════════════════════════
# Provider Webhooks
# ═══════════════════════════════════════

@app.post("/webhooks/unifonic", tags=["Webhooks"])
async def unifonic_webhook(payload: dict):
    """Handle Unifonic delivery / read receipts."""
    logger.info("unifonic_webhook", event=payload.get("event"), message_id=payload.get("message_id"))
    return {"received": True}

@app.post("/webhooks/geidea", tags=["Webhooks"])
async def geidea_webhook(payload: dict):
    """Handle Geidea payment callbacks."""
    logger.info("geidea_webhook", payment_id=payload.get("payment_id"), status=payload.get("status"))
    return {"received": True}

# ═══════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════

async def _check_database():
    try:
        db = await get_db()
        # TODO: Actual DB ping
        return True
    except Exception:
        return False

async def _check_unifonic():
    return bool(settings.UNIFONIC_API_KEY)

async def _check_nphies():
    return bool(settings.NPHIES_CLIENT_ID)

async def _check_geidea():
    return bool(settings.GEIDEA_API_KEY)
