import logging
from src.alerts.email_alerts import send_email
from src.alerts.sms_alerts import send_sms

class AlertPipeline:
    """ AI-Based Alert System for Shipment Delays, Compliance, and Maintenance """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    def trigger_alert(self, alert_type, alert_data):
        """ Triggers Alerts Based on AI Decisions """
        try:
            message = f"🚨 Alert: {alert_type} - Details: {alert_data}"
            logging.info(message)

            # Send Email Alert
            send_email("logistics@company.com", "Logistics Alert", message)

            # Send SMS Alert
            send_sms("+1234567890", message)

            return {"status": "Alert Sent", "details": message}
        except Exception as e:
            logging.error(f"Failed to send alert: {e}")
            return None
