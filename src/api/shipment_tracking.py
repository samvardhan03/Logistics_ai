from fastapi import APIRouter, HTTPException
from src.database.db_operations import DatabaseOperations

router = APIRouter(tags=["Shipment Tracking"])

db = DatabaseOperations()

@router.get("/{shipment_id}")
def get_shipment_status(shipment_id: str):
    """ Fetches real-time shipment details """
    shipment = db.get_shipment(shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment Not Found")
    return {"id": shipment.id, "status": shipment.status, "ETA": shipment.eta}

@router.put("/{shipment_id}/update")
def update_shipment_status(shipment_id: str, new_status: str):
    """ Updates shipment status (Delivered, In Transit, Delayed) """
    updated_shipment = db.update_shipment_status(shipment_id, new_status)
    if not updated_shipment:
        raise HTTPException(status_code=404, detail="Shipment Not Found")
    return {"message": "Shipment Status Updated", "new_status": updated_shipment.status}
