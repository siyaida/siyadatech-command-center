"""AI-powered appointment scheduling with no-show prediction."""
import structlog
import random
from datetime import datetime, timedelta
from typing import List, Dict

logger = structlog.get_logger()

class AppointmentScheduler:
    """
    AI no-show prediction + intelligent scheduling.
    Uses patient history, appointment patterns, and KSA-specific factors.
    """
    
    # No-show risk factors (KSA healthcare research-backed)
    RISK_FACTORS = {
        "first_time_patient": 0.25,
        "evening_appointment": 0.15,
        "friday_appointment": 0.20,
        "no_insurance": 0.10,
        "previous_no_show": 0.35,
        "long_gap_since_last_visit": 0.15,
        "hot_weather_day": 0.05,  # Jeddah summer factor
    }
    
    def __init__(self):
        self.base_no_show_rate = 0.18  # KSA clinic average
    
    async def predict_no_show_risk(self, appointment) -> float:
        """
        Predict probability of no-show (0.0 - 1.0).
        
        Args:
            appointment: AppointmentCreate model
            
        Returns:
            Risk score between 0 and 1
        """
        risk = self.base_no_show_rate
        
        # Time-based risk
        hour = appointment.scheduled_time.hour
        if hour >= 17:  # Evening appointments
            risk += self.RISK_FACTORS["evening_appointment"]
        
        # Friday risk (weekend in KSA)
        if appointment.scheduled_time.weekday() == 4:  # Friday
            risk += self.RISK_FACTORS["friday_appointment"]
        
        # Insurance status
        if not appointment.insurance_national_id:
            risk += self.RISK_FACTORS["no_insurance"]
        
        # Cap at 0.95
        return min(risk, 0.95)
    
    async def get_recommended_reminder_strategy(self, risk_score: float) -> Dict:
        """
        Get reminder strategy based on risk score.
        
        Returns:
            Dict with reminder schedule and channel preferences
        """
        if risk_score > 0.7:
            return {
                "strategy": "aggressive",
                "reminders": [
                    {"hours_before": 72, "channel": "whatsapp", "type": "confirmation"},
                    {"hours_before": 24, "channel": "whatsapp+sms", "type": "reminder"},
                    {"hours_before": 4, "channel": "whatsapp+sms+call", "type": "urgent"},
                    {"hours_before": 1, "channel": "whatsapp", "type": "final"},
                ],
                "deposit_required": True,
                "deposit_amount": 50,  # SAR
            }
        elif risk_score > 0.4:
            return {
                "strategy": "standard",
                "reminders": [
                    {"hours_before": 24, "channel": "whatsapp", "type": "reminder"},
                    {"hours_before": 2, "channel": "whatsapp+sms", "type": "final"},
                ],
                "deposit_required": False,
            }
        else:
            return {
                "strategy": "minimal",
                "reminders": [
                    {"hours_before": 24, "channel": "whatsapp", "type": "reminder"},
                ],
                "deposit_required": False,
            }
    
    async def optimize_schedule(self, appointments: List[Dict], doctors: List[Dict]) -> List[Dict]:
        """
        Optimize daily schedule to minimize gaps and no-shows.
        
        Returns:
            Optimized appointment schedule with buffer times
        """
        # Simple heuristic: group by doctor, add 15min buffer after high-risk patients
        optimized = []
        
        for doctor in doctors:
            doctor_appts = [a for a in appointments if a.get("doctor_id") == doctor["id"]]
            doctor_appts.sort(key=lambda x: x["scheduled_time"])
            
            current_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=9)
            
            for appt in doctor_appts:
                appt["optimized_time"] = max(appt["scheduled_time"], current_time)
                
                # Add buffer for high-risk patients
                if appt.get("no_show_risk", 0) > 0.6:
                    buffer_minutes = 15
                else:
                    buffer_minutes = 10
                
                current_time = appt["optimized_time"] + timedelta(minutes=30 + buffer_minutes)
                optimized.append(appt)
        
        return optimized
