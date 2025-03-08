from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API Routers
from src.api.shipment_tracking import router as shipment_router
from src.api.delay_prediction import router as delay_router
from src.api.route_optimization import router as route_router
from src.api.warehouse_management import router as warehouse_router
from src.api.predictive_maintenance import router as maintenance_router
from src.api.compliance_api import router as compliance_router

#Initialize FastAPI App
app = FastAPI(title="Logistics AI API", version="1.0.0", description="AI-powered Logistics API")

#Enable CORS for Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routes
app.include_router(shipment_router, prefix="/shipment")
app.include_router(delay_router, prefix="/delay")
app.include_router(route_router, prefix="/route")
app.include_router(warehouse_router, prefix="/warehouse")
app.include_router(maintenance_router, prefix="/maintenance")
app.include_router(compliance_router, prefix="/compliance")

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Logistics AI API is Running!"}
