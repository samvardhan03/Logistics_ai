from fastapi import APIRouter
from src.models.warehouse_ai import WarehouseAI

router = APIRouter(tags=["Warehouse Management"])
warehouse_ai = WarehouseAI()

@router.get("/{sku_id}")
def get_stock_levels(sku_id: str):
    """ Retrieves current stock levels for a given SKU """
    stock_data = warehouse_ai.get_stock(sku_id)
    return {"sku_id": sku_id, "stock_level": stock_data["stock"], "reorder_needed": stock_data["reorder_needed"]}
