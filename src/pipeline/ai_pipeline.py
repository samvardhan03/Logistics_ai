import logging
from src.models.transformer_model import DelayPredictionModel
from src.models.route_optimizer import RouteOptimizer
from src.models.warehouse_ai import WarehouseAI
from src.models.predictive_maintenance import MaintenanceAI

# Initialize AI models
delay_model = DelayPredictionModel()
route_optimizer = RouteOptimizer()
warehouse_ai = WarehouseAI()
maintenance_ai = MaintenanceAI()

class AIPipeline:
    """ Central AI Pipeline - Manages Execution of AI Models """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    def predict_shipment_delay(self, shipment_data):
        """ Uses Transformer Model to Predict Shipment Delays """
        try:
            prediction = delay_model.predict(shipment_data)
            logging.info(f"Delay Prediction: {prediction}")
            return prediction
        except Exception as e:
            logging.error(f"Delay Prediction Failed: {e}")
            return None

    def optimize_route(self, shipment_data):
        """ Uses AI Model to Optimize Delivery Routes """
        try:
            optimized_route = route_optimizer.find_best_route(shipment_data)
            logging.info(f"Optimized Route: {optimized_route}")
            return optimized_route
        except Exception as e:
            logging.error(f"Route Optimization Failed: {e}")
            return None

    def optimize_inventory(self, warehouse_data):
        """ Uses Warehouse AI to Optimize Stock Levels """
        try:
            inventory_plan = warehouse_ai.optimize_stock(warehouse_data)
            logging.info(f"Optimized Inventory Plan: {inventory_plan}")
            return inventory_plan
        except Exception as e:
            logging.error(f"Inventory Optimization Failed: {e}")
            return None

    def detect_maintenance_issues(self, equipment_data):
        """ Uses Predictive Maintenance AI to Detect Failures """
        try:
            maintenance_plan = maintenance_ai.detect_failures(equipment_data)
            logging.info(f"Predictive Maintenance Result: {maintenance_plan}")
            return maintenance_plan
        except Exception as e:
            logging.error(f"Predictive Maintenance Failed: {e}")
            return None
