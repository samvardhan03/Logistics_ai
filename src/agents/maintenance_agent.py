import logging
from src.models.predictive_maintenance import detect_failures
from src.database.db_operations import schedule_maintenance
from src.agents.agent_memory import AgentMemory

class MaintenanceAgent:
    """AI Agent for Predictive Equipment Monitoring"""

    def __init__(self):
        self.agent_name = "Maintenance AI"
        self.memory = AgentMemory()

    def monitor_and_fix_equipment(self, equipment_id):
        """AI-driven predictive maintenance for logistics equipment"""
        try:
            failure_risk = detect_failures(equipment_id)

            if failure_risk > 80:
                schedule_maintenance(equipment_id)
                self.memory.store_memory(self.agent_name, equipment_id, "Maintenance Scheduled")
                logging.info(f"Maintenance scheduled for Equipment {equipment_id}")

                return {"status": "scheduled", "equipment_id": equipment_id}
            else:
                self.memory.store_memory(self.agent_name, equipment_id, "No Action Required")
                return {"status": "no_action", "equipment_id": equipment_id}
        except Exception as e:
            logging.error(f"Predictive Maintenance Failed: {e}")
            return {"status": "error", "equipment_id": equipment_id}
