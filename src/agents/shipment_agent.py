import langgraph
from src.models.route_optimizer import optimize_route
from src.database.db_operations import update_shipment_route
from src.agents.agent_memory import AgentMemory

class ShipmentAgent(langgraph.Agent):
    def __init__(self):
        self.agent_name = "Shipment AI"
        self.memory = AgentMemory()

    def reroute_shipment(self, shipment_id):
        # AI suggests an optimal reroute
        new_route = optimize_route(shipment_id)

        # Apply the new route
        update_shipment_route(shipment_id, new_route)

        # Store new route decision in memory
        self.memory.store_memory(self.agent_name, shipment_id, new_route)

        return {"status": "rerouted", "shipment_id": shipment_id, "new_route": new_route}
