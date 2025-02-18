import logging
from src.models.warehouse_ai import warehouse_prediction
from src.database.db_operations import update_inventory
from src.agents.agent_memory import AgentMemory

class WarehouseAgent:
    """AI Agent for Warehouse Stock Optimization"""

    def __init__(self):
        self.agent_name = "Warehouse AI"
        self.memory = AgentMemory()

    def optimize_inventory(self, product_id):
        """Predict and optimize warehouse inventory levels"""
        try:
            predicted_stock = warehouse_prediction(product_id)
            update_inventory(product_id, predicted_stock)

            # Store inventory decision in memory
            self.memory.store_memory(self.agent_name, product_id, predicted_stock)
            logging.info(f"Inventory optimized for Product {product_id}")

            return {"status": "optimized", "product_id": product_id, "predicted_stock": predicted_stock}
        except Exception as e:
            logging.error(f"Inventory Optimization Failed: {e}")
            return {"status": "error", "product_id": product_id}
