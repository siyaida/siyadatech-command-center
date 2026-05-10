"""
Kafka event streaming for real-time clinic operations.
Produces events for: appointments, payments, patient actions.
"""
import json
import structlog
from datetime import datetime
from typing import Dict, Any
from kafka import KafkaProducer, KafkaConsumer
from app.config import settings

logger = structlog.get_logger()

class EventStream:
    """Kafka event producer for Ragaban clinic events."""
    
    def __init__(self):
        self.producer = None
        self._connected = False
    
    def _get_producer(self):
        if self.producer is None:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
            )
        return self.producer
    
    async def publish(self, topic: str, event_type: str, payload: Dict[str, Any], key: str = None):
        """Publish event to Kafka topic."""
        try:
            producer = self._get_producer()
            event = {
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "payload": payload,
                "source": "ragaban-api",
                "version": "1.0.0",
            }
            producer.send(topic, key=key, value=event)
            logger.info("kafka_event_published", topic=topic, event_type=event_type)
        except Exception as e:
            logger.error("kafka_publish_failed", topic=topic, error=str(e))
    
    async def appointment_created(self, appointment_id: str, patient_id: str, branch_id: str, scheduled_time: str):
        """Publish appointment created event."""
        await self.publish(
            topic="ragaban.appointments",
            event_type="appointment.created",
            key=appointment_id,
            payload={
                "appointment_id": appointment_id,
                "patient_id": patient_id,
                "branch_id": branch_id,
                "scheduled_time": scheduled_time,
            }
        )
    
    async def appointment_confirmed(self, appointment_id: str, channel: str, message_id: str):
        """Publish appointment confirmation event."""
        await self.publish(
            topic="ragaban.appointments",
            event_type="appointment.confirmed",
            key=appointment_id,
            payload={
                "appointment_id": appointment_id,
                "channel": channel,
                "message_id": message_id,
            }
        )
    
    async def payment_received(self, payment_id: str, patient_id: str, amount: float, method: str):
        """Publish payment received event."""
        await self.publish(
            topic="ragaban.payments",
            event_type="payment.received",
            key=payment_id,
            payload={
                "payment_id": payment_id,
                "patient_id": patient_id,
                "amount": amount,
                "currency": "SAR",
                "method": method,
            }
        )
    
    async def patient_registered(self, patient_id: str, national_id: str, branch_id: str):
        """Publish patient registration event."""
        await self.publish(
            topic="ragaban.patients",
            event_type="patient.registered",
            key=patient_id,
            payload={
                "patient_id": patient_id,
                "national_id": national_id,
                "branch_id": branch_id,
            }
        )
    
    async def claim_submitted(self, claim_id: str, patient_id: str, amount: float, insurer: str):
        """Publish insurance claim submission event."""
        await self.publish(
            topic="ragaban.insurance",
            event_type="claim.submitted",
            key=claim_id,
            payload={
                "claim_id": claim_id,
                "patient_id": patient_id,
                "amount": amount,
                "currency": "SAR",
                "insurer": insurer,
            }
        )
    
    async def no_show_detected(self, appointment_id: str, patient_id: str, branch_id: str, risk_score: float):
        """Publish no-show event for follow-up actions."""
        await self.publish(
            topic="ragaban.appointments",
            event_type="appointment.no_show",
            key=appointment_id,
            payload={
                "appointment_id": appointment_id,
                "patient_id": patient_id,
                "branch_id": branch_id,
                "risk_score": risk_score,
                "action": "reschedule_or_penalty",
            }
        )

class EventConsumer:
    """Kafka consumer for processing clinic events."""
    
    def __init__(self, topic: str, group_id: str):
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
    
    def start(self, handler):
        """Start consuming events with handler function."""
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=self.group_id,
            auto_offset_reset="latest",
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )
        
        for message in self.consumer:
            try:
                event = message.value
                handler(event)
            except Exception as e:
                logger.error("event_processing_failed", topic=self.topic, error=str(e))
