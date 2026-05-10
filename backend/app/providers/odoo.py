"""
Odoo ERP Integration Module
Syncs appointments, patients, and payments between Ragaban API and Odoo.
"""
import httpx
import structlog
from typing import Dict, List, Optional
from app.config import settings

logger = structlog.get_logger()

class OdooClient:
    """
    Odoo JSON-RPC client for Ragaban Clinics.
    Connects to self-hosted Odoo instance.
    """
    
    def __init__(self):
        self.base_url = settings.ODOO_URL or "http://odoo:8069"
        self.database = settings.ODOO_DATABASE or "ragaban"
        self.username = settings.ODOO_USERNAME or "admin"
        self.password = settings.ODOO_PASSWORD or "admin"
        self.uid = None
    
    async def authenticate(self) -> int:
        """Authenticate with Odoo and get user ID."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/jsonrpc",
                json={
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "common",
                        "method": "login",
                        "args": [self.database, self.username, self.password],
                    },
                    "id": 1,
                },
            )
            data = response.json()
            self.uid = data.get("result")
            logger.info("odoo_authenticated", uid=self.uid)
            return self.uid
    
    async def create_patient(self, patient_data: Dict) -> Dict:
        """Create patient in Odoo CRM/Contacts."""
        if not self.uid:
            await self.authenticate()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/jsonrpc",
                json={
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "object",
                        "method": "execute",
                        "args": [
                            self.database, self.uid, self.password,
                            "res.partner", "create",
                            {
                                "name": patient_data["name"],
                                "phone": patient_data["phone"],
                                "email": patient_data.get("email"),
                                "vat": patient_data.get("national_id"),  # Saudi national ID
                                "category_id": [(6, 0, [self._get_patient_tag_id()])],
                            },
                        ],
                    },
                    "id": 2,
                },
            )
            data = response.json()
            odoo_id = data.get("result")
            logger.info("odoo_patient_created", odoo_id=odoo_id, name=patient_data["name"])
            return {"odoo_id": odoo_id, "status": "created"}
    
    async def create_appointment(self, appointment_data: Dict) -> Dict:
        """Create appointment in Odoo Calendar/CRM."""
        if not self.uid:
            await self.authenticate()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/jsonrpc",
                json={
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "object",
                        "method": "execute",
                        "args": [
                            self.database, self.uid, self.password,
                            "calendar.event", "create",
                            {
                                "name": f"Appointment: {appointment_data['patient_name']}",
                                "start": appointment_data["scheduled_time"].isoformat(),
                                "stop": (appointment_data["scheduled_time"] + timedelta(hours=1)).isoformat(),
                                "description": appointment_data.get("reason", ""),
                                "location": appointment_data.get("branch_id", ""),
                                "partner_ids": [(6, 0, [appointment_data.get("odoo_partner_id")])],
                            },
                        ],
                    },
                    "id": 3,
                },
            )
            data = response.json()
            event_id = data.get("result")
            logger.info("odoo_appointment_created", event_id=event_id)
            return {"odoo_event_id": event_id, "status": "created"}
    
    async def sync_inventory(self, items: List[Dict]) -> Dict:
        """Sync medical inventory with Odoo Stock module."""
        if not self.uid:
            await self.authenticate()
        
        results = []
        for item in items:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/jsonrpc",
                    json={
                        "jsonrpc": "2.0",
                        "method": "call",
                        "params": {
                            "service": "object",
                            "method": "execute",
                            "args": [
                                self.database, self.uid, self.password,
                                "product.product", "search_read",
                                [[("name", "=", item["name"])]],
                                ["id", "qty_available"],
                            ],
                        },
                        "id": 4,
                    },
                )
                data = response.json()
                products = data.get("result", [])
                
                if products:
                    results.append({
                        "item": item["name"],
                        "odoo_id": products[0]["id"],
                        "current_stock": products[0]["qty_available"],
                        "predicted_need": item["predicted_need"],
                        "status": "ok" if products[0]["qty_available"] >= item["predicted_need"] else "reorder",
                    })
        
        return {"synced_items": results}
    
    def _get_patient_tag_id(self) -> int:
        """Get or create 'Patient' tag in Odoo."""
        # TODO: Implement actual tag lookup
        return 1

from datetime import timedelta
