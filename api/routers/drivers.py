from fastapi import APIRouter, HTTPException, Path, Body, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
from managers.user_manager import UserManager
from managers.ride_manager import RideManager
from models.user import Driver
from models.ride import VehicleType

router = APIRouter()
user_manager = UserManager()
ride_manager = RideManager()

# Pydantic models for request/response
class VehicleInfo(BaseModel):
    vehicle_id: str = Field(..., description="Vehicle ID")
    model: str = Field(..., description="Vehicle model")
    vehicle_type: str = Field(..., description="Vehicle type (BIKE, AUTO_RICKSHAW, SEDAN, SUV)")
    capacity: int = Field(..., description="Vehicle capacity", ge=1)

class DriverCreate(BaseModel):
    name: str = Field(..., description="Driver name")
    phone: str = Field(..., description="Driver phone number")
    vehicle: VehicleInfo = Field(..., description="Vehicle information")
    current_location: Tuple[float, float] = Field(..., description="Current location (latitude, longitude)")

class DriverResponse(BaseModel):
    id: str
    name: str
    phone: str
    vehicle: VehicleInfo
    current_location: Tuple[float, float]
    is_available: bool
    rating: float
    ride_history: List[str] = []

    class Config:
        from_attributes = True

class LocationUpdate(BaseModel):
    location: Tuple[float, float] = Field(..., description="New location (latitude, longitude)")

class AvailabilityUpdate(BaseModel):
    is_available: bool = Field(..., description="Availability status")

class AvailableDriversRequest(BaseModel):
    location: Tuple[float, float] = Field(..., description="Current location (latitude, longitude)")
    max_distance: float = Field(15.0, description="Maximum distance in kilometers", ge=0.0, le=50.0)
    vehicle_type: Optional[str] = Field(None, description="Filter by vehicle type")

class AvailableDriverResponse(BaseModel):
    id: str
    name: str
    vehicle_id: str
    vehicle_model: str
    vehicle_type: str
    rating: float
    distance: float

# Routes
@router.post("/", response_model=DriverResponse)
async def create_driver(driver_data: DriverCreate):
    """Register a new driver"""
    try:
        driver = user_manager.register_driver(
            driver_data.name,
            driver_data.phone,
            driver_data.vehicle.vehicle_id,
            driver_data.vehicle.model,
            driver_data.vehicle.vehicle_type,
            driver_data.vehicle.capacity,
            driver_data.current_location
        )
        # Register driver with ride manager
        ride_manager.register_driver(driver)
        return convert_to_response(driver)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[DriverResponse])
async def get_all_drivers():
    """Get all registered drivers"""
    drivers = user_manager.get_all_drivers()
    return [convert_to_response(driver) for driver in drivers]

@router.get("/available", response_model=List[DriverResponse])
async def get_available_drivers():
    """Get all available drivers"""
    drivers = ride_manager.get_available_drivers()
    return [convert_to_response(driver) for driver in drivers]

@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(driver_id: str = Path(..., description="The ID of the driver to get")):
    """Get a specific driver by ID"""
    driver = user_manager.get_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return convert_to_response(driver)

@router.put("/{driver_id}/location", response_model=DriverResponse)
async def update_driver_location(
    location_data: LocationUpdate,
    driver_id: str = Path(..., description="The ID of the driver to update")
):
    """Update a driver's current location"""
    success = user_manager.update_driver_location(driver_id, location_data.location)
    if not success:
        raise HTTPException(status_code=404, detail="Driver not found")
    return convert_to_response(user_manager.get_driver(driver_id))

@router.put("/{driver_id}/availability", response_model=DriverResponse)
async def update_driver_availability(
    availability_update: AvailabilityUpdate,
    driver_id: str = Path(..., description="The ID of the driver to update")
):
    """Update a driver's availability status"""
    driver = user_manager.get_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver.set_availability(availability_update.is_available)
    
    if availability_update.is_available:
        ride_manager.register_driver(driver)
    else:
        ride_manager.unregister_driver(driver)
    
    return convert_to_response(driver)

@router.post("/available", response_model=List[AvailableDriverResponse])
async def find_available_drivers(request: AvailableDriversRequest):
    """Find available drivers within a specified range"""
    try:
        # Get all available drivers from the ride manager
        all_available_drivers = ride_manager.get_available_drivers()
        
        # Import necessary modules for distance calculation
        from models.ride import Ride
        from models.user import Rider
        
        # Create a temporary ride object to use its distance calculation method
        temp_rider = Rider("Temporary", "0000000000")
        temp_ride = Ride(temp_rider, request.location, (0.0, 0.0))
        
        # Filter drivers by distance and optionally by vehicle type
        nearby_drivers = []
        for driver in all_available_drivers:
            # Calculate distance between request location and driver location
            distance = temp_ride._calculate_distance(request.location, driver.get_location())
            
            # Check if driver is within the specified range
            if distance <= request.max_distance:
                # If vehicle type filter is provided, check if it matches
                if request.vehicle_type is None or driver.vehicle.vehicle_type == request.vehicle_type:
                    nearby_drivers.append({
                        "id": driver.id,
                        "name": driver.name,
                        "vehicle_id": driver.vehicle.vehicle_id,
                        "vehicle_model": driver.vehicle.model,
                        "vehicle_type": driver.vehicle.vehicle_type,
                        "rating": driver.rating,
                        "distance": distance
                    })
        
        # Sort by distance (closest first)
        nearby_drivers.sort(key=lambda d: d["distance"])
        
        return nearby_drivers
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Helper function
def convert_to_response(driver: Driver) -> DriverResponse:
    """Convert Driver object to DriverResponse model"""
    vehicle_info = VehicleInfo(
        vehicle_id=driver.vehicle.vehicle_id,
        model=driver.vehicle.model,
        vehicle_type=driver.vehicle.vehicle_type,
        capacity=driver.vehicle.capacity
    )
    
    return DriverResponse(
        id=driver.id,
        name=driver.name,
        phone=driver.phone,
        vehicle=vehicle_info,
        current_location=driver.current_location,
        is_available=driver.is_available,
        rating=driver.rating,
        ride_history=driver.ride_history
    ) 