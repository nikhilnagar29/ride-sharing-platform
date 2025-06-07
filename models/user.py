from abc import ABC
from typing import Tuple, List, Optional
from uuid import uuid4

# this contain User class , Vehicle 
# and there are two type of user rider and driver

class User(ABC):
    def __init__(self, name: str, phone: str):
        self.id = str(uuid4())  # Keep public as it's needed for identification
        self._name = name
        self._phone = phone
        
    @property
    def name(self):
        return self._name
        
    @property
    def phone(self):
        return self._phone

class Rider(User):
    def __init__(self, name: str, phone: str, default_location: Tuple[float, float] = (0.0, 0.0)):
        super().__init__(name, phone)
        self._default_location = default_location
        self._current_location = default_location
        self._ride_history = []
    
    def update_location(self, location: Tuple[float, float]):
        self._current_location = location
    
    def get_location(self) -> Tuple[float, float]:
        return self._current_location
        
    @property
    def default_location(self):
        return self._default_location
        
    @property
    def current_location(self):
        return self._current_location
        
    @property
    def ride_history(self):
        return self._ride_history

class Vehicle:
    def __init__(self, vehicle_id: str, model: str, vehicle_type: str, capacity: int):
        self.vehicle_id = vehicle_id  # Keep public as it's used for identification
        self._model = model
        self._vehicle_type = vehicle_type
        self._capacity = capacity
        
    @property
    def model(self):
        return self._model
        
    @property
    def vehicle_type(self):
        return self._vehicle_type
        
    @property
    def capacity(self):
        return self._capacity

class Driver(User):
    def __init__(self, name: str, phone: str, vehicle: Vehicle, location: Tuple[float, float] = (0.0, 0.0)):
        super().__init__(name, phone)
        self.vehicle = vehicle  # Keep public as it's a complex object often accessed directly
        self._current_location = location
        self._is_available = True
        self._rating = 4.5  # Default rating
        self._ride_history = []
    
    def update_location(self, location: Tuple[float, float]):
        self._current_location = location
    
    def get_location(self) -> Tuple[float, float]:
        return self._current_location
    
    def set_availability(self, is_available: bool):
        self._is_available = is_available
    
    def update_rating(self, new_rating: float):
        # Simple average rating calculation
        total_rides = len(self._ride_history)
        if total_rides == 0:
            self._rating = new_rating
        else:
            self._rating = (self._rating * total_rides + new_rating) / (total_rides + 1)
            
    @property
    def current_location(self):
        return self._current_location
        
    @property
    def is_available(self):
        return self._is_available
        
    @property
    def rating(self):
        return self._rating
        
    @rating.setter
    def rating(self, value):
        self._rating = value
        
    @property
    def ride_history(self):
        return self._ride_history 