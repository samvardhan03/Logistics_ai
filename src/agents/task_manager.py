import langgraph
import logging
import redis  
from langgraph.graph import StateGraph
from enum import Enum
import json  
from src.agents.compliance_agent import ComplianceAgent
from src.agents.shipment_agent import ShipmentAgent
from src.agents.warehouse_agent import WarehouseAgent
from src.agents.maintenance_agent import MaintenanceAgent
from src.agents.agent_memory import AgentMemory

# Set up logging
logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Define State Enums for better tracking
class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class LogisticsState:
    """ Workflow State Tracking (Stores execution progress) """
    compliance_status: TaskStatus = TaskStatus.PENDING
    shipment_status: TaskStatus = TaskStatus.PENDING
    inventory_status: TaskStatus = TaskStatus.PENDING
    maintenance_status: TaskStatus = TaskStatus.PENDING
    event_id: str = ""  # Unique ID for tracking tasks


class TaskManager:
    """ Orchestrates all AI agents and manages DAG-based execution """

    def __init__(self):
        self.memory = AgentMemory()
        self.compliance_agent = ComplianceAgent()
        self.shipment_agent = ShipmentAgent()
        self.warehouse_agent = WarehouseAgent()
        self.maintenance_agent = MaintenanceAgent()

        # Initialize LangGraph Workflow DAG
        self.workflow = StateGraph(LogisticsState)
        
        # Define DAG Nodes (Each AI agent is a node in the workflow)
        self.workflow.add_node("check_compliance", self.check_compliance)
        self.workflow.add_node("reroute_shipment", self.reroute_shipment)
        self.workflow.add_node("optimize_inventory", self.optimize_inventory)
        self.workflow.add_node("monitor_equipment", self.monitor_equipment)

        #Define State Transitions (DAG dependencies)
        self.workflow.add_edge("check_compliance", "reroute_shipment")  
        self.workflow.add_edge("check_compliance", "optimize_inventory")  
        self.workflow.add_edge("reroute_shipment", "monitor_equipment")  

        #Enable Checkpointing (Using Redis for persistent AI workflow state tracking)
        self.workflow.set_checkpoint(RedisCheckpoint())

        self.app = self.workflow.compile()

# Compliance Agent Execution
    def check_compliance(self, state: LogisticsState):
        """ Checks and fixes compliance issues """
        if state.compliance_status == TaskStatus.COMPLETED:
            return state  # Skip execution if already done

        try:
            result = self.compliance_agent.check_and_fix_compliance(state.event_id)
            logging.info(f"Compliance Fix Triggered: {result}")
            state.compliance_status = TaskStatus.COMPLETED
        except Exception as e:
            logging.error(f"Compliance Agent Failed: {e}")
            state.compliance_status = TaskStatus.FAILED

        return state

    # Shipment Rerouting Execution (Runs only if shipment is delayed)
    def reroute_shipment(self, state: LogisticsState):
        """ AI-based shipment rerouting for delayed shipments """
        if state.shipment_status == TaskStatus.COMPLETED:
            return state  # Skip if already done

        try:
            result = self.shipment_agent.reroute_shipment(state.event_id)
            logging.info(f"Shipment Reroute Triggered: {result}")
            state.shipment_status = TaskStatus.COMPLETED
        except Exception as e:
            logging.error(f"Shipment Agent Failed: {e}")
            state.shipment_status = TaskStatus.FAILED

        return state

    # Warehouse Inventory Optimization Execution
    def optimize_inventory(self, state: LogisticsState):
        """ AI-powered warehouse stock optimization """
        if state.inventory_status == TaskStatus.COMPLETED:
            return state  

        try:
            result = self.warehouse_agent.optimize_inventory(state.event_id)
            logging.info(f"Inventory Optimization Triggered: {result}")
            state.inventory_status = TaskStatus.COMPLETED
        except Exception as e:
            logging.error(f"Warehouse Agent Failed: {e}")
            state.inventory_status = TaskStatus.FAILED

        return state

    # Predictive Equipment Maintenance Execution
    def monitor_equipment(self, state: LogisticsState):
        """ Predictive maintenance AI to prevent equipment failure """
        if state.maintenance_status == TaskStatus.COMPLETED:
            return state  # Skip execution if already done

        try:
            result = self.maintenance_agent.monitor_and_fix_equipment(state.event_id)
            logging.info(f"Predictive Maintenance Triggered: {result}")
            state.maintenance_status = TaskStatus.COMPLETED
        except Exception as e:
            logging.error(f"Maintenance Agent Failed: {e}")
            state.maintenance_status = TaskStatus.FAILED

        return state

    # Executes the AI Workflow using DAG-based Execution
    def execute_workflow(self, event_id):
        """ Executes the DAG-based AI workflow """
        state = LogisticsState(event_id=event_id)
        final_state = self.app.invoke(state)

        # Store execution in AI memory for learning-based decision-making
        self.memory.store_memory("TaskManager", event_id, {
            "compliance": final_state.compliance_status.value,
            "shipment": final_state.shipment_status.value,
            "inventory": final_state.inventory_status.value,
            "maintenance": final_state.maintenance_status.value
        })

        logging.info(f"Workflow Execution Complete: {final_state}")
        return final_state


  
