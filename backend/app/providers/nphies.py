import httpx
import structlog
from datetime import datetime, timedelta
from app.config import settings

logger = structlog.get_logger()

class NPHIESClient:
    """
    NPHIES (National Health Information Exchange & Services) FHIR R4 client.
    Mandatory for all KSA healthcare providers.
    
    APIs:
    - Patient $summary
    - Coverage $eligibility  
    - Claim $submit
    - Consent management
    """
    
    def __init__(self):
        self.client_id = settings.NPHIES_CLIENT_ID
        self.client_secret = settings.NPHIES_CLIENT_SECRET
        self.base_url = settings.NPHIES_BASE_URL
        self.token_url = settings.NPHIES_TOKEN_URL
        self._token = None
        self._token_expires = None
    
    async def _get_token(self) -> str:
        """OAuth2 client credentials flow for NPHIES."""
        if self._token and self._token_expires and datetime.utcnow() < self._token_expires:
            return self._token
        
        if not self.client_id or not self.client_secret:
            logger.error("nphies_credentials_missing")
            raise ValueError("NPHIES_CLIENT_ID and NPHIES_CLIENT_SECRET required")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": "nphies/patient.read nphies/coverage.read nphies/claim.write",
                },
            )
            data = response.json()
            self._token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self._token_expires = datetime.utcnow() + timedelta(seconds=expires_in - 60)
            logger.info("nphies_token_acquired", expires_in=expires_in)
            return self._token
    
    async def check_eligibility(self, national_id: str) -> dict:
        """
        Check insurance eligibility via NPHIES FHIR Coverage/$eligibility.
        
        Args:
            national_id: Saudi national ID (10 digits)
            
        Returns:
            Eligibility status, coverage details, insurer info
        """
        token = await self._get_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/fhir/Coverage/$eligibility",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/fhir+json",
                    "X-NPHIES-Provider-ID": settings.NPHIES_CLIENT_ID,
                },
                json={
                    "resourceType": "Parameters",
                    "parameter": [
                        {
                            "name": "nationalId",
                            "valueString": national_id,
                        },
                        {
                            "name": "providerId", 
                            "valueString": settings.NPHIES_CLIENT_ID,
                        },
                    ],
                },
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info("nphies_eligibility_success", national_id=national_id)
                return {
                    "eligible": data.get("eligible", True),
                    "coverage": data.get("coverage", {}),
                    "insurer": data.get("insurer", {}).get("display", "Unknown"),
                    "raw_response": data,
                }
            else:
                logger.error("nphies_eligibility_failed", 
                           national_id=national_id, 
                           status=response.status_code,
                           body=response.text)
                return {"eligible": False, "error": response.text}
    
    async def submit_claim(self, claim_data: dict) -> dict:
        """
        Submit insurance claim via NPHIES FHIR Claim/$submit.
        
        Args:
            claim_data: FHIR Claim resource or simplified dict with:
                - patient_id
                - national_id
                - diagnosis_codes (ICD-10)
                - procedure_codes (CPT/HCPCS)
                - total_amount (SAR)
                - items: list of service items
                
        Returns:
            Claim ID, status, tracking information
        """
        token = await self._get_token()
        
        # Build FHIR Claim resource
        fhir_claim = self._build_fhir_claim(claim_data)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/fhir/Claim/$submit",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/fhir+json",
                    "X-NPHIES-Provider-ID": settings.NPHIES_CLIENT_ID,
                },
                json=fhir_claim,
            )
            
            if response.status_code in (200, 201):
                data = response.json()
                claim_id = data.get("id", f"CLAIM-{datetime.utcnow().timestamp()}")
                logger.info("nphies_claim_submitted", claim_id=claim_id)
                return {
                    "claim_id": claim_id,
                    "status": "submitted",
                    "tracking_url": f"https://nphies.seha.sa/claims/{claim_id}",
                    "raw_response": data,
                }
            else:
                logger.error("nphies_claim_failed", status=response.status_code)
                return {"status": "failed", "error": response.text}
    
    def _build_fhir_claim(self, data: dict) -> dict:
        """Convert simplified claim data to FHIR R4 Claim resource."""
        return {
            "resourceType": "Claim",
            "id": data.get("claim_id", f"ragaban-{datetime.utcnow().timestamp()}"),
            "status": "active",
            "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "professional"}]},
            "use": "claim",
            "patient": {"reference": f"Patient/{data['patient_id']}"},
            "created": datetime.utcnow().isoformat(),
            "provider": {"reference": f"Organization/{settings.NPHIES_CLIENT_ID}"},
            "priority": {"coding": [{"code": "normal"}]},
            "insurance": [{
                "sequence": 1,
                "focal": True,
                "coverage": {"reference": f"Coverage/{data['national_id']}"},
            }],
            "diagnosis": [
                {"sequence": i+1, "diagnosisCodeableConcept": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": code}]}}
                for i, code in enumerate(data.get("diagnosis_codes", []))
            ],
            "item": [
                {
                    "sequence": i+1,
                    "productOrService": {"coding": [{"system": "http://www.ama-assn.org/go/cpt", "code": item.get("code")}]},
                    "unitPrice": {"value": item.get("price", 0), "currency": "SAR"},
                }
                for i, item in enumerate(data.get("items", []))
            ],
            "total": {"value": data.get("total_amount", 0), "currency": "SAR"},
        }
