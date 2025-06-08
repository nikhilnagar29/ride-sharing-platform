from fastapi import APIRouter, HTTPException, Path, Body, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
from managers.user_manager import UserManager
from models.user import Rider

router = APIRouter()
user_manager = UserManager()

# Pydantic models for request/response
class RiderCreate(BaseModel):
    name: str = Field(..., description="Rider name")
    phone: str = Field(..., description="Rider phone number")
    default_location: Tuple[float, float] = Field(..., description="Rider default location (latitude, longitude)")

class RiderResponse(BaseModel):
    id: str
    name: str
    phone: str
    default_location: Tuple[float, float]
    current_location: Tuple[float, float]
    ride_history: List[str] = []

    class Config:
        from_attributes = True

class LocationUpdate(BaseModel):
    location: Tuple[float, float] = Field(..., description="New location (latitude, longitude)")

# Routes
@router.post("/", response_model=RiderResponse)
async def create_rider(rider_data: RiderCreate):
    """Register a new rider"""
    try:
        rider = user_manager.register_rider(
            rider_data.name,
            rider_data.phone,
            rider_data.default_location
        )
        return convert_to_response(rider)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RiderResponse])
async def get_all_riders():
    """Get all registered riders"""
    riders = user_manager.get_all_riders()
    return [convert_to_response(rider) for rider in riders]

@router.get("/{rider_id}", response_model=RiderResponse)
async def get_rider(rider_id: str = Path(..., description="The ID of the rider to get")):
    """Get a specific rider by ID"""
    rider = user_manager.get_rider(rider_id)
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return convert_to_response(rider)

@router.put("/{rider_id}/location", response_model=RiderResponse)
async def update_rider_location(
    location_data: LocationUpdate,
    rider_id: str = Path(..., description="The ID of the rider to update")
):
    """Update a rider's current location"""
    success = user_manager.update_rider_location(rider_id, location_data.location)
    if not success:
        raise HTTPException(status_code=404, detail="Rider not found")
    return convert_to_response(user_manager.get_rider(rider_id))

# Helper function
def convert_to_response(rider: Rider) -> RiderResponse:
    """Convert Rider object to RiderResponse model"""
    return RiderResponse(
        id=rider.id,
        name=rider.name,
        phone=rider.phone,
        default_location=rider.default_location,
        current_location=rider.current_location,
        ride_history=rider.ride_history
    ) 