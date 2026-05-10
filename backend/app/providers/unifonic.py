import httpx
import structlog
from app.config import settings

logger = structlog.get_logger()

class UnifonicClient:
    """Saudi-born communication platform. SMS + WhatsApp Business API."""
    
    def __init__(self):
        self.api_key = settings.UNIFONIC_API_KEY
        self.base_url = settings.UNIFONIC_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    async def send_sms(self, phone: str, message: str, sender: str = "Ragaban") -> dict:
        """Send SMS via Unifonic — KSA-optimized routing."""
        if not self.api_key:
            logger.warning("unifonic_no_api_key", action="send_sms")
            return {"status": "skipped", "reason": "UNIFONIC_API_KEY not configured"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/messages",
                headers=self.headers,
                json={
                    "recipient": phone,
                    "body": message,
                    "sender": sender,
                    "language": "ar" if self._is_arabic(message) else "en",
                },
            )
            data = response.json()
            logger.info("unifonic_sms_sent", phone=phone, message_id=data.get("messageId"))
            return data
    
    async def send_whatsapp_appointment_confirmation(
        self, phone: str, appointment_time: str, branch: str, risk_score: float
    ) -> dict:
        """Send WhatsApp Business API message with appointment details."""
        if not self.api_key:
            return {"status": "skipped"}
        
        message = self._build_whatsapp_confirmation_message(
            appointment_time, branch, risk_score
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/whatsapp/messages",
                headers=self.headers,
                json={
                    "recipient": phone,
                    "type": "template",
                    "template": "ragaban_appointment_confirmation",
                    "language": "ar",
                    "params": {
                        "appointment_time": appointment_time,
                        "branch": branch,
                        "risk_level": "high" if risk_score > 0.7 else "low",
                    },
                },
            )
            return response.json()
    
    async def send_whatsapp_reminder(self, phone: str, appointment_time: str, branch: str) -> dict:
        """Send 24h/2h reminder via WhatsApp."""
        if not self.api_key:
            return {"status": "skipped"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/whatsapp/messages",
                headers=self.headers,
                json={
                    "recipient": phone,
                    "type": "template",
                    "template": "ragaban_appointment_reminder",
                    "language": "ar",
                    "params": {
                        "appointment_time": appointment_time,
                        "branch": branch,
                    },
                },
            )
            return response.json()
    
    def _build_whatsapp_confirmation_message(self, time: str, branch: str, risk: float) -> str:
        if self._is_arabic(time):
            return f"تم تأكيد موعدك في {time} في فرع {branch}"
        return f"Your appointment at {time} ({branch}) is confirmed."
    
    def _is_arabic(self, text: str) -> bool:
        return any("\u0600" <= c <= "\u06FF" for c in text)
