from fastapi import APIRouter
from src.models.predictive_maintenance import PredictiveMaintenanceAI

router = APIRouter(tags=["Predictive Maintenance"])
maintenance_ai = PredictiveMaintenanceAI()

@router.get("/{equipment_id}")
def monitor_equipment(equipment_id: str):
    """ AI detects upcoming equipment failures & suggests maintenance """
    maintenance_status = maintenance_ai.check_equipment(equipment_id)
    return {"equipment_id": equipment_id, "status": maintenance_status["status"], "maintenance_required": maintenance_status["needed"]}
