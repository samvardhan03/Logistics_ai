import requests
import logging
from src.database.db_operations import fetch_shipment_data, fetch_inventory_data

class DataPipeline:
    """ Fetches Real-Time Data for AI Processing """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    def fetch_google_maps_data(self, origin, destination):
        """ Fetches Traffic & ETA Data from Google Maps API """
        try:
            api_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key=YOUR_GOOGLE_MAPS_API_KEY"
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Fetched Google Maps Data: {data}")
            return data
        except Exception as e:
            logging.error(f"Failed to fetch Google Maps Data: {e}")
            return None

    def fetch_shipment_status(self, shipment_id):
        """ Fetches Real-Time Shipment Tracking Data """
        try:
            shipment_data = fetch_shipment_data(shipment_id)
            logging.info(f"Fetched Shipment Data: {shipment_data}")
            return shipment_data
        except Exception as e:
            logging.error(f"Failed to fetch shipment data: {e}")
            return None

    def fetch_inventory_status(self, warehouse_id):
        """ Fetches Inventory Data from Warehouse Database """
        try:
            inventory_data = fetch_inventory_data(warehouse_id)
            logging.info(f"Fetched Inventory Data: {inventory_data}")
            return inventory_data
        except Exception as e:
            logging.error(f"Failed to fetch inventory data: {e}")
            return None
