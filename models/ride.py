from enum import Enum
from typing import Tuple, List, Optional
from uuid import uuid4
from datetime import datetime
from models.user import Rider, Driver

class RideStatus(Enum):
    REQUESTED = "REQUESTED"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    DRIVER_EN_ROUTE = "DRIVER_EN_ROUTE"
    RIDE_IN_PROGRESS = "RIDE_IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class RideType(Enum):
    REGULAR = "REGULAR"
    CARPOOL = "CARPOOL"

class VehicleType(Enum):
    BIKE = "BIKE"
    AUTO_RICKSHAW = "AUTO_RICKSHAW"
    SEDAN = "SEDAN"
    SUV = "SUV"

class Ride:
    def __init__(self, rider: Rider, pickup_location: Tuple[float, float], 
                 dropoff_location: Tuple[float, float], 
                 vehicle_type: VehicleType = VehicleType.SEDAN,
                 ride_type: RideType = RideType.REGULAR):
        self.id = str(uuid4())
        self.rider = rider
        self.driver = None
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.vehicle_type = vehicle_type
        self.ride_type = ride_type
        self.status = RideStatus.REQUESTED
        self.request_time = datetime.now()
        self.start_time = None
        self.end_time = None
        self.fare = 0.0
        self.distance = self._calculate_distance(pickup_location, dropoff_location)
        self.observers = []
    
    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points"""
        return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5
    
    def assign_driver(self, driver: Driver) -> bool:
        if self.status != RideStatus.REQUESTED:
            return False
        
        self.driver = driver
        self.status = RideStatus.DRIVER_ASSIGNED
        driver.set_availability(False)
        self._notify_observers()
        return True
    
    def start_ride(self) -> bool:
        if self.status != RideStatus.DRIVER_ASSIGNED:
            return False
        
        self.status = RideStatus.DRIVER_EN_ROUTE
        self._notify_observers()
        return True
    
    def pickup_rider(self) -> bool:
        if self.status != RideStatus.DRIVER_EN_ROUTE:
            return False
        
        self.status = RideStatus.RIDE_IN_PROGRESS
        self.start_time = datetime.now()
        self._notify_observers()
        return True
    
    def complete_ride(self) -> bool:
        if self.status != RideStatus.RIDE_IN_PROGRESS:
            return False
        
        self.status = RideStatus.COMPLETED
        self.end_time = datetime.now()
        if self.driver:
            self.driver.set_availability(True)
            self.driver.ride_history.append(self.id)
        
        self.rider.ride_history.append(self.id)
        self._notify_observers()
        return True
    
    def cancel_ride(self) -> bool:
        if self.status in [RideStatus.COMPLETED, RideStatus.CANCELLED]:
            return False
        
        self.status = RideStatus.CANCELLED
        if self.driver:
            self.driver.set_availability(True)
        
        self._notify_observers()
        return True
    
    def register_observer(self, observer):
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
    
    def _notify_observers(self):
        for observer in self.observers:
            observer.update(self) 