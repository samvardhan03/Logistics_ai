from sqlalchemy.orm import Session
from src.database.db_config import SessionLocal
from src.models.database_models import Shipment, Inventory, ComplianceRule

class DatabaseOperations:
    """ Handles CRUD Operations for Logistics AI """

    def __init__(self):
        self.db: Session = SessionLocal()

    def add_shipment(self, shipment_data):
        """ Adds a new shipment record """
        shipment = Shipment(**shipment_data)
        self.db.add(shipment)
        self.db.commit()
        return shipment

    def get_shipment(self, shipment_id):
        """ Retrieves a shipment by ID """
        return self.db.query(Shipment).filter(Shipment.id == shipment_id).first()

    def update_shipment_status(self, shipment_id, new_status):
        """ Updates shipment delivery status """
        shipment = self.get_shipment(shipment_id)
        if shipment:
            shipment.status = new_status
            self.db.commit()
            return shipment
        return None

    def delete_shipment(self, shipment_id):
        """ Deletes a shipment record """
        shipment = self.get_shipment(shipment_id)
        if shipment:
            self.db.delete(shipment)
            self.db.commit()
            return True
        return False

    def close(self):
        """ Closes database session """
        self.db.close()
