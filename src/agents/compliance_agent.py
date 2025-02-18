import logging
from src.retrieval.hybrid_search import hybrid_search
from src.database.db_operations import update_shipment_compliance
from src.agents.agent_memory import AgentMemory

class ComplianceAgent:
    """AI Agent for Automated Compliance Fixes"""

    def __init__(self):
        self.agent_name = "Compliance AI"
        self.memory = AgentMemory()

    def check_and_fix_compliance(self, shipment_id):
        """Check and fix compliance issues using Hybrid Search"""
        try:
            compliance_data = hybrid_search(f"Missing docs for shipment {shipment_id}")
            update_shipment_compliance(shipment_id, compliance_data)

            # Store compliance update in memory
            self.memory.store_memory(self.agent_name, shipment_id, compliance_data)
            logging.info(f"Compliance fix applied for Shipment {shipment_id}")

            return {"status": "fixed", "shipment_id": shipment_id, "compliance_data": compliance_data}
        except Exception as e:
            logging.error(f"Compliance Fix Failed: {e}")
            return {"status": "error", "shipment_id": shipment_id}
