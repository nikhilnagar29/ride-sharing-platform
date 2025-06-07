from abc import ABC
from typing import Tuple, List, Optional
from uuid import uuid4

# this contain User class , Vehicle 
# and there are two type of user rider and driver

class User(ABC):
    def __init__(self, name: str, phone: str):
        self.id = str(uuid4())
        self.name = name
        self.phone = phone

class Rider(User):
    def __init__(self, name: str, phone: str, default_location: Tuple[float, float] = (0.0, 0.0)):
        super().__init__(name, phone)
        self.default_location = default_location
        self.current_location = default_location
        self.ride_history = []
    
    def update_location(self, location: Tuple[float, float]):
        self.current_location = location
    
    def get_location(self) -> Tuple[float, float]:
        return self.current_location

class Vehicle:
    def __init__(self, vehicle_id: str, model: str, vehicle_type: str, capacity: int):
        self.vehicle_id = vehicle_id
        self.model = model
        self.vehicle_type = vehicle_type
        self.capacity = capacity

class Driver(User):
    def __init__(self, name: str, phone: str, vehicle: Vehicle, location: Tuple[float, float] = (0.0, 0.0)):
        super().__init__(name, phone)
        self.vehicle = vehicle
        self.current_location = location
        self.is_available = True
        self.rating = 4.5  # Default rating
        self.ride_history = []
    
    def update_location(self, location: Tuple[float, float]):
        self.current_location = location
    
    def get_location(self) -> Tuple[float, float]:
        return self.current_location
    
    def set_availability(self, is_available: bool):
        self.is_available = is_available
    
    def update_rating(self, new_rating: float):
        # Simple average rating calculation
        total_rides = len(self.ride_history)
        if total_rides == 0:
            self.rating = new_rating
        else:
            self.rating = (self.rating * total_rides + new_rating) / (total_rides + 1) 