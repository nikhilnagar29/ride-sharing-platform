from abc import ABC, abstractmethod
from typing import List, Optional
from models.user import Driver
from models.ride import Ride

class DriverMatchingStrategy(ABC):
    """Abstract strategy for matching drivers to rides"""
    
    @abstractmethod
    def find_driver(self, ride: Ride, available_drivers: List[Driver]) -> Optional[Driver]:
        """Find the best driver for a ride based on the strategy"""
        pass

class NearestDriverStrategy(DriverMatchingStrategy):
    """Strategy that matches the nearest available driver"""
    
    def find_driver(self, ride: Ride, available_drivers: List[Driver]) -> Optional[Driver]:
        if not available_drivers:
            return None
        
        # Filter drivers by vehicle type
        matching_drivers = [driver for driver in available_drivers 
                           if driver.vehicle.vehicle_type == ride.vehicle_type.value]
        
        if not matching_drivers:
            return None
        
        # Find the nearest driver
        nearest_driver = min(matching_drivers, 
                            key=lambda driver: self._calculate_distance(
                                driver.get_location(), ride.pickup_location))
        
        return nearest_driver
    
    def _calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5

class HighestRatedDriverStrategy(DriverMatchingStrategy):
    """Strategy that matches the highest rated available driver"""
    
    def find_driver(self, ride: Ride, available_drivers: List[Driver]) -> Optional[Driver]:
        if not available_drivers:
            return None
        
        # Filter drivers by vehicle type
        matching_drivers = [driver for driver in available_drivers 
                           if driver.vehicle.vehicle_type == ride.vehicle_type.value]
        
        if not matching_drivers:
            return None
        
        # Find the highest rated driver
        highest_rated_driver = max(matching_drivers, key=lambda driver: driver.rating)
        
        return highest_rated_driver 