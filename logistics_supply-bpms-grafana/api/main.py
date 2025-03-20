from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
import pandas as pd
from models.optimization import LogisticsOptimizer

app = FastAPI(
    title="SupplyChainOptimizer API",
    description="API para otimização de logística e cadeia de suprimentos",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize optimizer
optimizer = LogisticsOptimizer()

# Data models
class Location(BaseModel):
    latitude: float
    longitude: float
    demand: Optional[float] = None

class InventoryOptimizationRequest(BaseModel):
    demand_data: List[float]
    holding_cost: float
    ordering_cost: float
    lead_time: int

class RouteOptimizationRequest(BaseModel):
    locations: List[Location]
    vehicle_capacity: float

class TransportationOptimizationRequest(BaseModel):
    origins: List[Location]
    destinations: List[Location]
    supplies: List[float]
    demands: List[float]
    costs: List[List[float]]

class ClusterAnalysisRequest(BaseModel):
    locations: List[Location]
    num_clusters: int

# API endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/optimize/inventory")
async def optimize_inventory(request: InventoryOptimizationRequest):
    try:
        demand_df = pd.DataFrame({'demand': request.demand_data})
        result = optimizer.optimize_inventory(
            demand_data=demand_df,
            holding_cost=request.holding_cost,
            ordering_cost=request.ordering_cost,
            lead_time=request.lead_time
        )
        return {"message": "Inventory optimization successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize/routes")
async def optimize_routes(request: RouteOptimizationRequest):
    try:
        locations = [(loc.latitude, loc.longitude) for loc in request.locations]
        demands = [loc.demand or 0 for loc in request.locations]
        result = optimizer.optimize_routes(
            locations=locations,
            demands=demands,
            vehicle_capacity=request.vehicle_capacity
        )
        return {"message": "Route optimization successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize/transportation")
async def optimize_transportation(request: TransportationOptimizationRequest):
    try:
        origins = [(loc.latitude, loc.longitude) for loc in request.origins]
        destinations = [(loc.latitude, loc.longitude) for loc in request.destinations]
        result = optimizer.optimize_transportation(
            origins=origins,
            destinations=destinations,
            supplies=request.supplies,
            demands=request.demands,
            costs=request.costs
        )
        return {"message": "Transportation optimization successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/clusters")
async def analyze_clusters(request: ClusterAnalysisRequest):
    try:
        locations = [(loc.latitude, loc.longitude) for loc in request.locations]
        result = optimizer.cluster_locations(
            locations=locations,
            num_clusters=request.num_clusters
        )
        return {"message": "Cluster analysis successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize/warehouse-location")
async def optimize_warehouse_location(request: ClusterAnalysisRequest):
    try:
        locations = [(loc.latitude, loc.longitude) for loc in request.locations]
        demands = [loc.demand or 1.0 for loc in request.locations]
        result = optimizer.optimize_warehouse_location(
            locations=locations,
            demands=demands
        )
        return {"message": "Warehouse location optimization successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 