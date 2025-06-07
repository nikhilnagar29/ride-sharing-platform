from abc import ABC, abstractmethod
from typing import List, Optional
from models.user import Driver
from models.ride import Ride
import math

class DriverMatchingStrategy(ABC):
    """Abstract strategy for matching drivers to rides"""
    
    @abstractmethod
    def find_driver(self, ride: Ride, available_drivers: List[Driver]) -> Optional[Driver]:
        """Find the best driver for a ride based on the strategy"""
        pass
    
    def _is_within_range(self, driver_location, pickup_location, ride, max_distance=10.0):
        """Check if driver is within max_distance km of pickup location using Haversine distance"""
        # Use the ride's _calculate_distance method which implements Haversine formula
        return ride._calculate_distance(driver_location, pickup_location) <= max_distance

class NearestDriverStrategy(DriverMatchingStrategy):
    """Strategy that matches the nearest available driver within 10km"""
    
    def find_driver(self, ride: Ride, available_drivers: List[Driver]) -> Optional[Driver]:
        if not available_drivers:
            return None
        
        # Filter drivers by vehicle type and range (10km)
        matching_drivers = [
            driver for driver in available_drivers 
            if driver.vehicle.vehicle_type == ride.vehicle_type.value and
            self._is_within_range(driver.get_location(), ride.pickup_location, ride)
        ]
        
        if not matching_drivers:
            return None
        
        # Find the nearest driver using ride's Haversine distance calculation
        nearest_driver = min(matching_drivers, 
                            key=lambda driver: ride._calculate_distance(
                                driver.get_location(), ride.pickup_location))
        
        return nearest_driver

class HighestRatedDriverStrategy(DriverMatchingStrategy):
    """Strategy that matches the highest rated available driver within 10km"""
    
    def find_driver(self, ride: Ride, available_drivers: List[Driver]) -> Optional[Driver]:
        if not available_drivers:
            return None
        
        # Filter drivers by vehicle type and range (10km)
        matching_drivers = [
            driver for driver in available_drivers 
            if driver.vehicle.vehicle_type == ride.vehicle_type.value and
            self._is_within_range(driver.get_location(), ride.pickup_location, ride)
        ]
        
        if not matching_drivers:
            return None
        
        # Find the highest rated driver
        highest_rated_driver = max(matching_drivers, key=lambda driver: driver.rating)
        
        return highest_rated_driver 