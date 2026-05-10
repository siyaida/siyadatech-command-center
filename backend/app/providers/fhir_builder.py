"""
FHIR R4 resource builders for NPHIES integration.
Generates compliant FHIR resources for Saudi healthcare.
"""
from datetime import datetime
from typing import Dict, List, Optional

class FHIRBuilder:
    """Build FHIR R4 resources for NPHIES compliance."""
    
    @staticmethod
    def build_patient(
        national_id: str,
        name: str,
        phone: str,
        birth_date: Optional[str] = None,
        gender: Optional[str] = None,
    ) -> Dict:
        """Build FHIR Patient resource with Saudi national ID."""
        family_name, given_name = FHIRBuilder._split_name(name)
        
        patient = {
            "resourceType": "Patient",
            "identifier": [
                {
                    "system": "https://nphies.seha.sa/identifier/national-id",
                    "value": national_id,
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "NNKSA",
                                "display": "National ID (KSA)",
                            }
                        ]
                    },
                }
            ],
            "name": [
                {
                    "use": "official",
                    "family": family_name,
                    "given": [given_name],
                }
            ],
            "telecom": [
                {
                    "system": "phone",
                    "value": phone,
                    "use": "mobile",
                }
            ],
        }
        
        if birth_date:
            patient["birthDate"] = birth_date
        if gender:
            patient["gender"] = gender.lower()
        
        return patient
    
    @staticmethod
    def build_coverage(
        patient_id: str,
        national_id: str,
        insurer_code: str,
        policy_number: Optional[str] = None,
    ) -> Dict:
        """Build FHIR Coverage resource for insurance."""
        return {
            "resourceType": "Coverage",
            "status": "active",
            "beneficiary": {"reference": f"Patient/{patient_id}"},
            "subscriber": {"reference": f"Patient/{patient_id}"},
            "subscriberId": national_id,
            "identifier": [
                {
                    "system": "https://nphies.seha.sa/identifier/policy-number",
                    "value": policy_number or national_id,
                }
            ],
            "payor": [
                {
                    "type": "Organization",
                    "identifier": {
                        "system": "https://nphies.seha.sa/identifier/insurer-code",
                        "value": insurer_code,
                    },
                }
            ],
        }
    
    @staticmethod
    def build_encounter(
        patient_id: str,
        encounter_id: str,
        start_time: datetime,
        encounter_class: str = "AMB",  # AMB = ambulatory
        service_type: str = "medical-spa",
    ) -> Dict:
        """Build FHIR Encounter resource for clinic visit."""
        return {
            "resourceType": "Encounter",
            "id": encounter_id,
            "status": "in-progress",
            "class": {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": encounter_class,
            },
            "type": [
                {
                    "coding": [
                        {
                            "system": "https://nphies.seha.sa/CodeSystem/service-type",
                            "code": service_type,
                        }
                    ]
                }
            ],
            "subject": {"reference": f"Patient/{patient_id}"},
            "period": {
                "start": start_time.isoformat(),
            },
        }
    
    @staticmethod
    def build_observation(
        patient_id: str,
        observation_type: str,
        value: float,
        unit: str,
        encounter_id: Optional[str] = None,
    ) -> Dict:
        """Build FHIR Observation for vitals or measurements."""
        obs = {
            "resourceType": "Observation",
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "vital-signs",
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": observation_type,
                    }
                ]
            },
            "subject": {"reference": f"Patient/{patient_id}"},
            "effectiveDateTime": datetime.utcnow().isoformat(),
            "valueQuantity": {
                "value": value,
                "unit": unit,
                "system": "http://unitsofmeasure.org",
                "code": unit,
            },
        }
        
        if encounter_id:
            obs["encounter"] = {"reference": f"Encounter/{encounter_id}"}
        
        return obs
    
    @staticmethod
    def build_bundle(resources: List[Dict], bundle_type: str = "transaction") -> Dict:
        """Build FHIR Bundle for batch submission."""
        entries = []
        for resource in resources:
            entry = {
                "resource": resource,
                "request": {
                    "method": "POST",
                    "url": resource["resourceType"],
                },
            }
            if "id" in resource:
                entry["fullUrl"] = f"urn:uuid:{resource['id']}"
            entries.append(entry)
        
        return {
            "resourceType": "Bundle",
            "type": bundle_type,
            "entry": entries,
        }
    
    @staticmethod
    def _split_name(full_name: str) -> tuple:
        """Split Arabic/English name into family and given."""
        parts = full_name.strip().split()
        if len(parts) == 1:
            return parts[0], ""
        # Last part is family name (Arabic convention)
        return parts[-1], " ".join(parts[:-1])
