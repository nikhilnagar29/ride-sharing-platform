from fastapi import APIRouter, HTTPException, Path, Body, Query, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from enum import Enum

from managers.user_manager import UserManager
from managers.ride_manager import RideManager
from models.ride import Ride, VehicleType, RideType, RideStatus
from models.user import Rider, Driver
from strategies.driver_matching import NearestDriverStrategy, HighestRatedDriverStrategy
from strategies.pricing import BasePricingStrategy, SurgePricingDecorator, DiscountDecorator

router = APIRouter()
user_manager = UserManager()
ride_manager = RideManager()

# Pydantic models
class VehicleTypeEnum(str, Enum):
    BIKE = "BIKE"
    AUTO_RICKSHAW = "AUTO_RICKSHAW"
    SEDAN = "SEDAN"
    SUV = "SUV"

class RideTypeEnum(str, Enum):
    REGULAR = "REGULAR"
    CARPOOL = "CARPOOL"

class RideStatusEnum(str, Enum):
    REQUESTED = "REQUESTED"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    DRIVER_EN_ROUTE = "DRIVER_EN_ROUTE"
    RIDE_IN_PROGRESS = "RIDE_IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class DriverMatchingStrategyEnum(str, Enum):
    NEAREST = "NEAREST"
    HIGHEST_RATED = "HIGHEST_RATED"

class PricingStrategyEnum(str, Enum):
    BASE = "BASE"
    SURGE = "SURGE"
    DISCOUNT = "DISCOUNT"

class RideCreate(BaseModel):
    rider_id: str = Field(..., description="ID of the rider requesting the ride")
    pickup_location: Tuple[float, float] = Field(..., description="Pickup location (latitude, longitude)")
    dropoff_location: Tuple[float, float] = Field(..., description="Dropoff location (latitude, longitude)")
    vehicle_type: VehicleTypeEnum = Field(VehicleTypeEnum.SEDAN, description="Requested vehicle type")
    ride_type: RideTypeEnum = Field(RideTypeEnum.REGULAR, description="Type of ride")
    driver_matching_strategy: DriverMatchingStrategyEnum = Field(
        DriverMatchingStrategyEnum.NEAREST, 
        description="Strategy for matching drivers"
    )
    pricing_strategy: PricingStrategyEnum = Field(
        PricingStrategyEnum.BASE, 
        description="Pricing strategy to use"
    )
    surge_multiplier: Optional[float] = Field(None, description="Surge pricing multiplier (if applicable)")
    discount_percentage: Optional[float] = Field(None, description="Discount percentage (if applicable)")

class FareEstimateRequest(BaseModel):
    pickup_location: Tuple[float, float] = Field(..., description="Pickup location (latitude, longitude)")
    dropoff_location: Tuple[float, float] = Field(..., description="Dropoff location (latitude, longitude)")
    vehicle_type: VehicleTypeEnum = Field(VehicleTypeEnum.SEDAN, description="Requested vehicle type")
    pricing_strategy: PricingStrategyEnum = Field(
        PricingStrategyEnum.BASE, 
        description="Pricing strategy to use"
    )
    surge_multiplier: Optional[float] = Field(None, description="Surge pricing multiplier (if applicable)")
    discount_percentage: Optional[float] = Field(None, description="Discount percentage (if applicable)")

class FareEstimateResponse(BaseModel):
    estimated_fare: float
    distance: float
    vehicle_type: str
    pricing_strategy: str
    base_fare: float
    per_km_rate: float

class DriverInfo(BaseModel):
    id: str
    name: str
    phone: str
    vehicle_id: str
    vehicle_model: str
    vehicle_type: str
    rating: float

class RideResponse(BaseModel):
    id: str
    rider_id: str
    driver: Optional[DriverInfo] = None
    pickup_location: Tuple[float, float]
    dropoff_location: Tuple[float, float]
    vehicle_type: str
    ride_type: str
    status: str
    request_time: datetime
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    fare: float
    distance: float

# Routes
@router.post("/", response_model=RideResponse)
async def request_ride(ride_data: RideCreate):
    """Request a new ride"""
    try:
        # Get the rider
        rider = user_manager.get_rider(ride_data.rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        
        # Set driver matching strategy
        if ride_data.driver_matching_strategy == DriverMatchingStrategyEnum.NEAREST:
            ride_manager.set_driver_matching_strategy(NearestDriverStrategy())
        else:
            ride_manager.set_driver_matching_strategy(HighestRatedDriverStrategy())
        
        # Set pricing strategy
        base_strategy = BasePricingStrategy()
        if ride_data.pricing_strategy == PricingStrategyEnum.SURGE:
            multiplier = ride_data.surge_multiplier or 1.5
            strategy = SurgePricingDecorator(base_strategy, multiplier)
            ride_manager.set_pricing_strategy(strategy)
        elif ride_data.pricing_strategy == PricingStrategyEnum.DISCOUNT:
            percentage = ride_data.discount_percentage or 10.0
            strategy = DiscountDecorator(base_strategy, percentage)
            ride_manager.set_pricing_strategy(strategy)
        else:
            ride_manager.set_pricing_strategy(base_strategy)
        
        # Request the ride
        vehicle_type = VehicleType[ride_data.vehicle_type]
        
        if ride_data.ride_type == RideTypeEnum.REGULAR:
            ride = ride_manager.request_ride(
                rider, 
                ride_data.pickup_location, 
                ride_data.dropoff_location, 
                vehicle_type
            )
        else:
            ride = ride_manager.request_carpool(
                rider, 
                ride_data.pickup_location, 
                ride_data.dropoff_location, 
                vehicle_type
            )
        
        if not ride:
            raise HTTPException(status_code=400, detail="Failed to create ride. No available drivers.")
        
        return convert_to_response(ride)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RideResponse])
async def get_all_rides():
    """Get all rides"""
    print("Total Riders:", len(user_manager.get_all_riders()), "Total Drivers:", len(user_manager.get_all_drivers()))
    rides = list(ride_manager.rides.values())
    return [convert_to_response(ride) for ride in rides]

@router.get("/active", response_model=List[RideResponse])
async def get_active_rides():
    """Get all active rides"""
    rides = list(ride_manager.active_rides.values())
    return [convert_to_response(ride) for ride in rides]

@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(ride_id: str = Path(..., description="The ID of the ride to get")):
    """Get a specific ride by ID"""
    ride = ride_manager.get_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return convert_to_response(ride)

@router.post("/estimate", response_model=FareEstimateResponse)
async def estimate_fare(fare_request: FareEstimateRequest):
    """Estimate the fare for a ride without creating a ride request"""
    try:
        # Create a temporary ride object to calculate distance
        from models.ride import Ride, VehicleType, RideType
        from models.user import Rider
        
        # Create a temporary rider (not saved)
        temp_rider = Rider("Temporary", "0000000000")
        
        # Create a temporary ride to calculate distance
        vehicle_type = VehicleType[fare_request.vehicle_type]
        temp_ride = Ride(
            temp_rider, 
            fare_request.pickup_location, 
            fare_request.dropoff_location, 
            vehicle_type,
            RideType.REGULAR
        )
        
        # Set pricing strategy
        base_strategy = BasePricingStrategy()
        if fare_request.pricing_strategy == PricingStrategyEnum.SURGE:
            multiplier = fare_request.surge_multiplier or 1.5
            strategy = SurgePricingDecorator(base_strategy, multiplier)
        elif fare_request.pricing_strategy == PricingStrategyEnum.DISCOUNT:
            percentage = fare_request.discount_percentage or 10.0
            strategy = DiscountDecorator(base_strategy, percentage)
        else:
            strategy = base_strategy
        
        # Calculate estimated fare
        estimated_fare = strategy.calculate_fare(temp_ride)
        
        # Get base price components for transparency
        base_fare = base_strategy._get_base_fare(vehicle_type)
        per_km_rate = base_strategy._get_per_km_rate(vehicle_type)
        
        return FareEstimateResponse(
            estimated_fare=estimated_fare,
            distance=temp_ride.distance,
            vehicle_type=fare_request.vehicle_type,
            pricing_strategy=fare_request.pricing_strategy,
            base_fare=base_fare,
            per_km_rate=per_km_rate
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{ride_id}/start", response_model=RideResponse)
async def start_ride(ride_id: str = Path(..., description="The ID of the ride to start")):
    """Start a ride (driver en route to pickup)"""
    success = ride_manager.start_ride(ride_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to start ride")
    return convert_to_response(ride_manager.get_ride(ride_id))

@router.put("/{ride_id}/pickup", response_model=RideResponse)
async def pickup_rider(ride_id: str = Path(..., description="The ID of the ride to update")):
    """Mark rider as picked up (ride in progress)"""
    success = ride_manager.pickup_rider(ride_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to pickup rider")
    return convert_to_response(ride_manager.get_ride(ride_id))

@router.put("/{ride_id}/complete", response_model=RideResponse)
async def complete_ride(ride_id: str = Path(..., description="The ID of the ride to complete")):
    """Complete a ride"""
    success = ride_manager.complete_ride(ride_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to complete ride")
    return convert_to_response(ride_manager.get_ride(ride_id))

@router.put("/{ride_id}/cancel", response_model=RideResponse)
async def cancel_ride(ride_id: str = Path(..., description="The ID of the ride to cancel")):
    """Cancel a ride"""
    success = ride_manager.cancel_ride(ride_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to cancel ride")
    return convert_to_response(ride_manager.get_ride(ride_id))

# Helper function
def convert_to_response(ride: Ride) -> RideResponse:
    """Convert Ride object to RideResponse model"""
    response_data = {
        "id": ride.id,
        "rider_id": ride.rider.id,
        "pickup_location": ride.pickup_location,
        "dropoff_location": ride.dropoff_location,
        "vehicle_type": ride.vehicle_type.value,
        "ride_type": ride.ride_type.value,
        "status": ride.status.value,
        "request_time": ride.request_time,
        "start_time": ride.start_time,
        "end_time": ride.end_time,
        "fare": ride.fare,
        "distance": ride.distance,
        "driver": None
    }
    
    if ride.driver:
        response_data["driver"] = DriverInfo(
            id=ride.driver.id,
            name=ride.driver.name,
            phone=ride.driver.phone,
            vehicle_id=ride.driver.vehicle.vehicle_id,
            vehicle_model=ride.driver.vehicle.model,
            vehicle_type=ride.driver.vehicle.vehicle_type,
            rating=ride.driver.rating
        )
    
    return RideResponse(**response_data) 