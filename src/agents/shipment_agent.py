import logging
from src.models.route_optimizer import optimize_route
from src.database.db_operations import update_shipment_route
from src.agents.agent_memory import AgentMemory

class ShipmentAgent:
    """AI Agent for Autonomous Shipment Rerouting"""

    def __init__(self):
        self.agent_name = "Shipment AI"
        self.memory = AgentMemory()

    def reroute_shipment(self, shipment_id):
        """AI-powered shipment rerouting based on live tracking data"""
        try:
            new_route = optimize_route(shipment_id)
            update_shipment_route(shipment_id, new_route)

            # Store new route in memory
            self.memory.store_memory(self.agent_name, shipment_id, new_route)
            logging.info(f"Shipment {shipment_id} rerouted to {new_route}")

            return {"status": "rerouted", "shipment_id": shipment_id, "new_route": new_route}
        except Exception as e:
            logging.error(f"Shipment Reroute Failed: {e}")
            return {"status": "error", "shipment_id": shipment_id}
