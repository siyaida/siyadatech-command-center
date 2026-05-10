import httpx
import structlog
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from app.config import settings

logger = structlog.get_logger()

class STCCloudClient:
    """
    STC Cloud — Tier-1 Saudi cloud provider.
    Data residency guarantee, NCA-compliant, PDPL-ready.
    Uses Google Cloud-compatible APIs (STC Cloud is GCP-based).
    """
    
    def __init__(self):
        self.credentials_path = settings.STC_CLOUD_CREDENTIALS
        self.project_id = None
        self._credentials = None
        self._token = None
    
    def _get_credentials(self):
        """Load service account credentials from JSON file."""
        if not self.credentials_path:
            raise ValueError("STC_CLOUD_CREDENTIALS not configured")
        
        if self._credentials is None:
            self._credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            self.project_id = self._credentials.project_id
        
        return self._credentials
    
    def _get_token(self):
        """Get OAuth2 access token for API calls."""
        if self._token is None or self._token.expired:
            creds = self._get_credentials()
            creds.refresh(Request())
            self._token = creds.token
        return self._token
    
    async def list_vms(self, zone: str = "me-central1-a") -> list:
        """List compute instances in a zone."""
        token = self._get_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://compute.googleapis.com/compute/v1/projects/{self.project_id}/zones/{zone}/instances",
                headers={"Authorization": f"Bearer {token}"},
            )
            data = response.json()
            return data.get("items", [])
    
    async def create_vm(self, name: str, zone: str = "me-central1-a", machine_type: str = "n1-standard-2") -> dict:
        """Create a new VM instance."""
        token = self._get_token()
        
        payload = {
            "name": name,
            "machineType": f"zones/{zone}/machineTypes/{machine_type}",
            "disks": [{
                "boot": True,
                "initializeParams": {
                    "sourceImage": "projects/debian-cloud/global/images/family/debian-12",
                    "diskSizeGb": "50",
                },
            }],
            "networkInterfaces": [{
                "network": "global/networks/default",
                "accessConfigs": [{"type": "ONE_TO_ONE_NAT"}],
            }],
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://compute.googleapis.com/compute/v1/projects/{self.project_id}/zones/{zone}/instances",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json=payload,
            )
            return response.json()
    
    async def upload_to_storage(self, bucket: str, object_name: str, file_data: bytes, content_type: str = "application/octet-stream") -> dict:
        """Upload file to STC Cloud Storage (S3-compatible)."""
        token = self._get_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://storage.googleapis.com/upload/storage/v1/b/{bucket}/o?uploadType=media&name={object_name}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": content_type,
                },
                content=file_data,
            )
            return response.json()
    
    async def get_storage_url(self, bucket: str, object_name: str, expires_minutes: int = 60) -> str:
        """Get signed URL for private storage object."""
        from google.cloud import storage
        
        if not self.credentials_path:
            raise ValueError("STC_CLOUD_CREDENTIALS not configured")
        
        client = storage.Client.from_service_account_json(self.credentials_path)
        blob = client.bucket(bucket).blob(object_name)
        
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expires_minutes),
            method="GET",
        )
        return url

from datetime import timedelta
