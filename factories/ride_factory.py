from typing import Tuple
from models.ride import Ride, VehicleType, RideType
from models.user import Rider

class RideFactory:
    """Factory for creating different types of rides"""
    
    @staticmethod
    def create_regular_ride(rider: Rider, pickup_location: Tuple[float, float], 
                          dropoff_location: Tuple[float, float], 
                          vehicle_type: VehicleType = VehicleType.SEDAN) -> Ride:
        """Create a regular ride"""
        return Ride(rider, pickup_location, dropoff_location, vehicle_type, RideType.REGULAR)
    
    @staticmethod
    def create_carpool_ride(rider: Rider, pickup_location: Tuple[float, float], 
                          dropoff_location: Tuple[float, float], 
                          vehicle_type: VehicleType = VehicleType.SEDAN) -> Ride:
        """Create a carpool ride"""
        # For carpool rides, we only allow vehicles with capacity > 2
        if vehicle_type in [VehicleType.SEDAN, VehicleType.SUV]:
            return Ride(rider, pickup_location, dropoff_location, vehicle_type, RideType.CARPOOL)
        else:
            # Default to sedan if inappropriate vehicle type selected for carpool
            return Ride(rider, pickup_location, dropoff_location, VehicleType.SEDAN, RideType.CARPOOL) 
 