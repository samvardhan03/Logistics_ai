from fastapi import APIRouter, Query
from src.models.route_optimizer import RouteOptimizer

router = APIRouter(tags=["Route Optimization"])
optimizer = RouteOptimizer()

@router.get("/optimize")
def get_optimized_route(source: str, destination: str):
    """ Returns AI-optimized route for delivery """
    optimized_route = optimizer.optimize(source, destination)
    return {"optimized_route": optimized_route}
