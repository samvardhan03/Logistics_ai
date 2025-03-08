from fastapi import APIRouter
from src.models.transformer_model import DelayPredictionModel

router = APIRouter(tags=["Delay Prediction"])
model = DelayPredictionModel()

@router.get("/{shipment_id}")
def predict_shipment_delay(shipment_id: str):
    """ Predicts shipment delay risk & adjusted ETA """
    delay_data = model.predict_delay(shipment_id)
    return {"shipment_id": shipment_id, "ETA": delay_data["eta"], "delay_risk": delay_data["risk_percentage"]}
