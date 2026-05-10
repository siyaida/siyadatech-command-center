import httpx
import structlog
from app.config import settings

logger = structlog.get_logger()

class GeideaClient:
    """
    Geidea Payment Gateway — SAMA licensed, KSA-native.
    Supports mada, Visa, Mastercard, Apple Pay.
    Arabic checkout UI. Lower fees than international gateways.
    """
    
    def __init__(self):
        self.api_key = settings.GEIDEA_API_KEY
        self.merchant_id = settings.GEIDEA_MERCHANT_ID
        self.base_url = settings.GEIDEA_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    async def create_payment(
        self,
        amount: float,
        currency: str = "SAR",
        description: str = "Ragaban Clinic Services",
        callback_url: str | None = None,
        customer_email: str | None = None,
        customer_phone: str | None = None,
    ) -> dict:
        """
        Create a payment session. Returns checkout URL for redirect.
        
        Args:
            amount: Amount in SAR
            currency: SAR (default)
            description: Payment description
            callback_url: Webhook URL for payment status updates
            customer_email: Optional customer email
            customer_phone: Optional customer phone (KSA format)
            
        Returns:
            Payment session with checkout_url
        """
        if not self.api_key:
            logger.warning("geidea_no_api_key")
            raise ValueError("GEIDEA_API_KEY not configured")
        
        payload = {
            "amount": float(amount),
            "currency": currency,
            "description": description,
            "merchantReferenceId": f"ragaban-{datetime.utcnow().timestamp()}",
            "callbackUrl": callback_url or "https://ragaban.siyada-cybersecurity.com/webhooks/geidea",
            "returnUrl": "https://ragaban.siyada-cybersecurity.com/payments/success",
            "language": "ar",
            "customer": {},
        }
        
        if customer_email:
            payload["customer"]["email"] = customer_email
        if customer_phone:
            payload["customer"]["phone"] = customer_phone
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/payments",
                headers=self.headers,
                json=payload,
            )
            
            data = response.json()
            
            if response.status_code in (200, 201):
                logger.info("geidea_payment_created", 
                           amount=amount, 
                           payment_id=data.get("paymentId"))
                return {
                    "payment_id": data["paymentId"],
                    "checkout_url": data["checkoutUrl"],
                    "status": "created",
                    "amount": amount,
                    "currency": currency,
                }
            else:
                logger.error("geidea_payment_failed", status=response.status_code, body=data)
                raise HTTPException(status_code=502, detail=f"Geidea error: {data}")
    
    async def verify_payment(self, payment_id: str) -> dict:
        """Verify payment status after callback."""
        if not self.api_key:
            raise ValueError("GEIDEA_API_KEY not configured")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/payments/{payment_id}",
                headers=self.headers,
            )
            data = response.json()
            
            logger.info("geidea_payment_verified", 
                       payment_id=payment_id, 
                       status=data.get("status"))
            return {
                "payment_id": payment_id,
                "status": data.get("status", "unknown"),
                "amount": data.get("amount"),
                "paid_at": data.get("paidAt"),
                "raw": data,
            }
    
    async def refund_payment(self, payment_id: str, amount: float | None = None) -> dict:
        """Process refund for a completed payment."""
        if not self.api_key:
            raise ValueError("GEIDEA_API_KEY not configured")
        
        payload = {"paymentId": payment_id}
        if amount:
            payload["amount"] = float(amount)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/payments/{payment_id}/refund",
                headers=self.headers,
                json=payload,
            )
            data = response.json()
            
            logger.info("geidea_refund_processed", 
                       payment_id=payment_id, 
                       status=data.get("status"))
            return {
                "refund_id": data.get("refundId"),
                "status": data.get("status"),
                "amount": amount,
                "raw": data,
            }

from datetime import datetime
from fastapi import HTTPException
