import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoints:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_readiness_without_providers(self):
        response = client.get("/ready")
        # Should return 503 if providers not configured
        assert response.status_code in [200, 503]
        data = response.json()
        assert "ready" in data
        assert "checks" in data

class TestPatientEndpoints:
    def test_create_patient(self):
        payload = {
            "national_id": "1234567890",
            "name": "Ahmed Al-Saud",
            "phone": "+966512345678",
            "email": "ahmed@example.com",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "branch_preference": "jeddah-main",
        }
        response = client.post("/patients", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["national_id"] == "1234567890"
        assert data["name"] == "Ahmed Al-Saud"
    
    def test_create_patient_invalid_national_id(self):
        payload = {
            "national_id": "12345",  # Too short
            "name": "Test",
            "phone": "+966512345678",
        }
        response = client.post("/patients", json=payload)
        assert response.status_code == 422

class TestAppointmentEndpoints:
    def test_create_appointment(self):
        payload = {
            "patient_id": "demo-patient-001",
            "patient_phone": "+966512345678",
            "branch_id": "jeddah-main",
            "department": "medical-spa",
            "scheduled_time": "2026-05-20T10:00:00",
            "reason": "Follow-up visit",
            "insurance_national_id": "1234567890",
        }
        response = client.post("/appointments", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "confirmed"
        assert "no_show_risk" in data
        assert 0 <= data["no_show_risk"] <= 1

class TestInsuranceEndpoints:
    def test_eligibility_without_nphies_config(self):
        response = client.get("/insurance/eligibility/1234567890")
        # Should fail with 503 if NPHIES not configured
        assert response.status_code == 503
        assert "NPHIES" in response.json()["detail"]
    
    def test_claim_submission_without_nphies_config(self):
        payload = {
            "patient_id": "demo-patient-001",
            "national_id": "1234567890",
            "diagnosis_codes": ["A01"],
            "total_amount": 500,
            "items": [{"code": "99213", "price": 500}],
        }
        response = client.post("/insurance/claims", json=payload)
        assert response.status_code == 503

class TestPaymentEndpoints:
    def test_create_payment_without_geidea_config(self):
        payload = {
            "patient_id": "demo-patient-001",
            "amount": 350,
            "method": "mada",
            "description": "Medical spa consultation",
        }
        response = client.post("/payments", json=payload)
        # Should fail with 503 if Geidea not configured
        assert response.status_code == 503

class TestAnalyticsEndpoints:
    def test_dashboard_metrics(self):
        response = client.get("/analytics/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "aggregated" in data
        assert "branches" in data
        assert "trends" in data
    
    def test_no_show_predictions(self):
        response = client.get("/analytics/no-show-prediction?days=7")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 7
        assert all("predicted_no_shows" in day for day in data)

class TestWebhookEndpoints:
    def test_unifonic_webhook(self):
        payload = {"event": "message_delivered", "message_id": "msg-123"}
        response = client.post("/webhooks/unifonic", json=payload)
        assert response.status_code == 200
        assert response.json()["received"] is True
    
    def test_geidea_webhook(self):
        payload = {"payment_id": "pay-123", "status": "completed"}
        response = client.post("/webhooks/geidea", json=payload)
        assert response.status_code == 200
        assert response.json()["received"] is True
