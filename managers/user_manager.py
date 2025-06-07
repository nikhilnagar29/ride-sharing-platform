from typing import Dict, List, Optional, Tuple
from models.user import User, Rider, Driver, Vehicle
from models.ride import VehicleType

class UserManager:
    """Singleton manager for handling users in the system"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the user manager"""
        self.riders: Dict[str, Rider] = {}  # Dictionary of all riders
        self.drivers: Dict[str, Driver] = {}  # Dictionary of all drivers
    
    def register_rider(self, name: str, phone: str, default_location: Tuple[float, float] = (0.0, 0.0)) -> Rider:
        """Register a new rider in the system"""
        rider = Rider(name, phone, default_location)
        self.riders[rider.id] = rider
        return rider
    
    def register_driver(self, name: str, phone: str, vehicle_id: str, model: str, 
                       vehicle_type: str, capacity: int, 
                       location: Tuple[float, float] = (0.0, 0.0)) -> Driver:
        """Register a new driver in the system"""
        vehicle = Vehicle(vehicle_id, model, vehicle_type, capacity)
        driver = Driver(name, phone, vehicle, location)
        self.drivers[driver.id] = driver
        return driver
    
    def get_rider(self, rider_id: str) -> Optional[Rider]:
        """Get a rider by ID"""
        return self.riders.get(rider_id)
    
    def get_driver(self, driver_id: str) -> Optional[Driver]:
        """Get a driver by ID"""
        return self.drivers.get(driver_id)
    
    def get_all_riders(self) -> List[Rider]:
        """Get all riders"""
        return list(self.riders.values())
    
    def get_all_drivers(self) -> List[Driver]:
        """Get all drivers"""
        return list(self.drivers.values())
    
    def update_rider_location(self, rider_id: str, location: Tuple[float, float]) -> bool:
        """Update a rider's location"""
        rider = self.get_rider(rider_id)
        if rider:
            rider.update_location(location)
            return True
        return False
    
    def update_driver_location(self, driver_id: str, location: Tuple[float, float]) -> bool:
        """Update a driver's location"""
        driver = self.get_driver(driver_id)
        if driver:
            driver.update_location(location)
            return True
        return False 