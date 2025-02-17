import langgraph
from src.retrieval.hybrid_search import hybrid_search
from src.database.db_operations import update_shipment_compliance
from src.agents.agent_memory import AgentMemory

class ComplianceAgent(langgraph.Agent):
    def __init__(self):
        self.agent_name = "Compliance AI"
        self.memory = AgentMemory()

    def check_and_fix_compliance(self, shipment_id):
        # Retrieve missing compliance rules
        compliance_data = hybrid_search(f"Missing docs for shipment {shipment_id}")

        update_shipment_compliance(shipment_id, compliance_data)

        self.memory.store_memory(self.agent_name, shipment_id, compliance_data)

        return {"status": "fixed", "shipment_id": shipment_id, "compliance_data": compliance_data}
