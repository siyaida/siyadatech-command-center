"""
OpenMRS Integration Module
Syncs patients, appointments, and encounters with OpenMRS EHR.
"""
import httpx
import structlog
from typing import Dict, List, Optional
from datetime import datetime
from app.config import settings

logger = structlog.get_logger()

class OpenMRSClient:
    """
    OpenMRS REST API client for Ragaban Clinics.
    Connects to self-hosted OpenMRS instance.
    """
    
    def __init__(self):
        self.base_url = settings.OPENMRS_URL or "http://openmrs:8080/openmrs"
        self.username = settings.OPENMRS_USERNAME or "admin"
        self.password = settings.OPENMRS_PASSWORD or "Admin123"
        self.session = None
    
    async def _get_session(self) -> Dict:
        """Authenticate with OpenMRS and get session."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/ws/rest/v1/session",
                auth=(self.username, self.password),
            )
            data = response.json()
            self.session = data
            logger.info("openmrs_authenticated", authenticated=data.get("authenticated"))
            return data
    
    async def create_patient(self, patient_data: Dict) -> Dict:
        """Create patient in OpenMRS with Saudi national ID."""
        if not self.session:
            await self._get_session()
        
        # Build OpenMRS patient payload
        payload = {
            "person": {
                "names": [
                    {
                        "givenName": patient_data.get("given_name", ""),
                        "familyName": patient_data.get("family_name", ""),
                    }
                ],
                "gender": patient_data.get("gender", "M").upper(),
                "birthdate": patient_data.get("date_of_birth"),
                "addresses": [
                    {
                        "cityVillage": patient_data.get("city", "Jeddah"),
                        "country": "Saudi Arabia",
                    }
                ],
            },
            "identifiers": [
                {
                    "identifier": patient_data["national_id"],
                    "identifierType": "National ID (KSA)",
                    "location": "Ragaban Main Clinic",
                }
            ],
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/ws/rest/v1/patient",
                auth=(self.username, self.password),
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            data = response.json()
            openmrs_uuid = data.get("uuid")
            logger.info("openmrs_patient_created", uuid=openmrs_uuid, name=patient_data.get("name"))
            return {"openmrs_uuid": openmrs_uuid, "status": "created"}
    
    async def create_encounter(self, encounter_data: Dict) -> Dict:
        """Create encounter (visit) in OpenMRS."""
        if not self.session:
            await self._get_session()
        
        payload = {
            "patient": encounter_data["patient_uuid"],
            "encounterType": encounter_data.get("encounter_type", "Consultation"),
            "encounterDatetime": encounter_data["scheduled_time"].isoformat(),
            "location": encounter_data.get("location_uuid", "Ragaban Main"),
            "obs": encounter_data.get("observations", []),
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/ws/rest/v1/encounter",
                auth=(self.username, self.password),
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            data = response.json()
            encounter_uuid = data.get("uuid")
            logger.info("openmrs_encounter_created", uuid=encounter_uuid)
            return {"openmrs_uuid": encounter_uuid, "status": "created"}
    
    async def add_observation(self, patient_uuid: str, concept: str, value: str, encounter_uuid: Optional[str] = None) -> Dict:
        """Add observation (vital, measurement) to patient record."""
        if not self.session:
            await self._get_session()
        
        payload = {
            "person": patient_uuid,
            "concept": concept,
            "obsDatetime": datetime.utcnow().isoformat(),
            "value": value,
        }
        
        if encounter_uuid:
            payload["encounter"] = encounter_uuid
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/ws/rest/v1/obs",
                auth=(self.username, self.password),
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            data = response.json()
            return {"openmrs_uuid": data.get("uuid"), "status": "created"}
    
    async def search_patients(self, query: str) -> List[Dict]:
        """Search patients by name or national ID."""
        if not self.session:
            await self._get_session()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/ws/rest/v1/patient",
                auth=(self.username, self.password),
                params={"q": query, "v": "full"},
            )
            data = response.json()
            results = data.get("results", [])
            return [
                {
                    "uuid": p["uuid"],
                    "name": p["display"],
                    "identifiers": [i["identifier"] for i in p.get("identifiers", [])],
                }
                for p in results
            ]
    
    async def get_patient_record(self, patient_uuid: str) -> Dict:
        """Get full patient record including encounters and observations."""
        if not self.session:
            await self._get_session()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/ws/rest/v1/patient/{patient_uuid}",
                auth=(self.username, self.password),
                params={"v": "full"},
            )
            return response.json()
    
    async def sync_from_ragaban_api(self, patient_id: str, national_id: str, name: str) -> Dict:
        """Sync patient from Ragaban API to OpenMRS."""
        # Check if patient exists
        existing = await self.search_patients(national_id)
        
        if existing:
            logger.info("openmrs_patient_exists", uuid=existing[0]["uuid"])
            return {"status": "existing", "openmrs_uuid": existing[0]["uuid"]}
        
        # Create new patient
        family, given = self._split_name(name)
        return await self.create_patient({
            "national_id": national_id,
            "given_name": given,
            "family_name": family,
        })
    
    def _split_name(self, full_name: str) -> tuple:
        """Split name for OpenMRS format."""
        parts = full_name.strip().split()
        if len(parts) == 1:
            return parts[0], ""
        return parts[-1], " ".join(parts[:-1])
