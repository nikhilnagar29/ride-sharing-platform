from enum import Enum
from typing import Tuple, List, Optional
from uuid import uuid4
from datetime import datetime
from models.user import Rider, Driver
import math

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
        self._rider = rider
        self._driver = None
        self._pickup_location = pickup_location
        self._dropoff_location = dropoff_location
        self._vehicle_type = vehicle_type
        self._ride_type = ride_type
        self._status = RideStatus.REQUESTED
        self._request_time = datetime.now()
        self._start_time = None
        self._end_time = None
        self._fare = 0.0
        self._distance = self._calculate_distance(pickup_location, dropoff_location)
        self._observers = []
    
    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate distance in kilometers between two points using the Haversine formula"""
        # Unpack the coordinates
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in kilometers
        r = 6371.0
        return c * r
    
    def assign_driver(self, driver: Driver) -> bool:
        if self._status != RideStatus.REQUESTED:
            return False
        
        self._driver = driver
        self._status = RideStatus.DRIVER_ASSIGNED
        driver.set_availability(False)
        self._notify_observers()
        return True
    
    def start_ride(self) -> bool:
        if self._status != RideStatus.DRIVER_ASSIGNED:
            return False
        
        self._status = RideStatus.DRIVER_EN_ROUTE
        self._notify_observers()
        return True
    
    def pickup_rider(self) -> bool:
        if self._status != RideStatus.DRIVER_EN_ROUTE:
            return False
        
        self._status = RideStatus.RIDE_IN_PROGRESS
        self._start_time = datetime.now()
        self._notify_observers()
        return True
    
    def complete_ride(self) -> bool:
        if self._status != RideStatus.RIDE_IN_PROGRESS:
            return False
        
        self._status = RideStatus.COMPLETED
        self._end_time = datetime.now()
        if self._driver:
            self._driver.set_availability(True)
            self._driver.ride_history.append(self.id)
        
        self._rider.ride_history.append(self.id)
        self._notify_observers()
        return True
    
    def cancel_ride(self) -> bool:
        if self._status in [RideStatus.COMPLETED, RideStatus.CANCELLED]:
            return False
        
        self._status = RideStatus.CANCELLED
        if self._driver:
            self._driver.set_availability(True)
        
        self._notify_observers()
        return True
    
    def register_observer(self, observer):
        self._observers.append(observer)
    
    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self):
        for observer in self._observers:
            observer.update(self)
            
    # Properties to access private attributes
    @property
    def rider(self):
        return self._rider
    
    @property
    def driver(self):
        return self._driver
    
    @property
    def pickup_location(self):
        return self._pickup_location
    
    @property
    def dropoff_location(self):
        return self._dropoff_location
    
    @property
    def vehicle_type(self):
        return self._vehicle_type
    
    @property
    def ride_type(self):
        return self._ride_type
    
    @property
    def status(self):
        return self._status
    
    @property
    def request_time(self):
        return self._request_time
    
    @property
    def start_time(self):
        return self._start_time
    
    @property
    def end_time(self):
        return self._end_time
    
    @property
    def fare(self):
        return self._fare
    
    @fare.setter
    def fare(self, value):
        self._fare = value
    
    @property
    def distance(self):
        return self._distance
    
    @property
    def observers(self):
        return self._observers 