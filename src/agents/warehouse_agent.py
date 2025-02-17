import langgraph
from src.models.warehouse_ai import warehouse_prediction
from src.database.db_operations import update_inventory
from src.agents.agent_memory import AgentMemory

class WarehouseAgent(langgraph.Agent):
    def __init__(self):
        self.agent_name = "Warehouse AI"
        self.memory = AgentMemory()

    def optimize_inventory(self, product_id):
        # Predict stock levels
        predicted_stock = warehouse_prediction(product_id)

        update_inventory(product_id, predicted_stock)

        self.memory.store_memory(self.agent_name, product_id, predicted_stock)

        return {"status": "optimized", "product_id": product_id, "predicted_stock": predicted_stock}
