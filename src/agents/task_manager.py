import langgraph
from src.agents.compliance_agent import ComplianceAgent
from src.agents.shipment_agent import ShipmentAgent
from src.agents.warehouse_agent import WarehouseAgent
from src.agents.maintenance_agent import MaintenanceAgent

class TaskManager:
    def __init__(self):
        self.workflow = langgraph.Workflow("Logistics_Agentic_Workflow")

        # Register AI Agents
        self.compliance_agent = ComplianceAgent()
        self.shipment_agent = ShipmentAgent()
        self.warehouse_agent = WarehouseAgent()
        self.maintenance_agent = MaintenanceAgent()

        # Define Task Execution Flow
        self.workflow.add_step(self.compliance_agent.check_and_fix_compliance)
        self.workflow.add_step(self.shipment_agent.reroute_shipment)
        self.workflow.add_step(self.warehouse_agent.optimize_inventory)
        self.workflow.add_step(self.maintenance_agent.monitor_and_fix_equipment)

    def execute_workflow(self, task, task_id):
        return self.workflow.run_step(task, task_id)
