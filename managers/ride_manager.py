from typing import Dict, List, Optional, Tuple
from models.ride import Ride, RideStatus
from models.user import Driver, Rider
from strategies.driver_matching import DriverMatchingStrategy, NearestDriverStrategy
from strategies.pricing import PricingStrategy, BasePricingStrategy
from observers.notification import RiderNotificationObserver, DriverNotificationObserver, SystemLogObserver
from factories.ride_factory import RideFactory

class RideManager:
    """Singleton manager for handling rides in the system"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RideManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the ride manager"""
        self.rides: Dict[str, Ride] = {}  # Dictionary of all rides
        self.active_rides: Dict[str, Ride] = {}  # Dictionary of active rides
        self.available_drivers: List[Driver] = []  # List of available drivers
        self.driver_matching_strategy: DriverMatchingStrategy = NearestDriverStrategy()
        self.pricing_strategy: PricingStrategy = BasePricingStrategy()
    
    def register_driver(self, driver: Driver) -> None:
        """Register a new driver in the system"""
        if driver not in self.available_drivers and driver.is_available:
            self.available_drivers.append(driver)
    
    def unregister_driver(self, driver: Driver) -> None:
        """Unregister a driver from the system"""
        if driver in self.available_drivers:
            self.available_drivers.remove(driver)
    
    def set_driver_matching_strategy(self, strategy: DriverMatchingStrategy) -> None:
        """Set the driver matching strategy"""
        self.driver_matching_strategy = strategy
    
    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        """Set the pricing strategy"""
        self.pricing_strategy = strategy
    
    def request_ride(self, rider: Rider, pickup_location: Tuple[float, float], 
                    dropoff_location: Tuple[float, float], vehicle_type) -> Optional[Ride]:
        """Request a new ride"""
        # Create a new ride using the factory
        ride = RideFactory.create_regular_ride(rider, pickup_location, dropoff_location, vehicle_type)
        
        # Add observers for notifications
        ride.register_observer(RiderNotificationObserver())
        ride.register_observer(DriverNotificationObserver())
        ride.register_observer(SystemLogObserver())
        
        # Store the ride
        self.rides[ride.id] = ride
        self.active_rides[ride.id] = ride
        
        # Try to find a driver
        self._assign_driver(ride)
        
        return ride
    
    def request_carpool(self, rider: Rider, pickup_location: Tuple[float, float], 
                       dropoff_location: Tuple[float, float], vehicle_type) -> Optional[Ride]:
        """Request a new carpool ride"""
        # Create a new carpool ride using the factory
        ride = RideFactory.create_carpool_ride(rider, pickup_location, dropoff_location, vehicle_type)
        
        # Add observers for notifications
        ride.register_observer(RiderNotificationObserver())
        ride.register_observer(DriverNotificationObserver())
        ride.register_observer(SystemLogObserver())
        
        # Store the ride
        self.rides[ride.id] = ride
        self.active_rides[ride.id] = ride
        
        # Try to find a driver
        self._assign_driver(ride)
        
        return ride
    
    def _assign_driver(self, ride: Ride) -> bool:
        """Assign a driver to a ride using the current matching strategy"""
        driver = self.driver_matching_strategy.find_driver(ride, self.available_drivers)
        
        if driver:
            ride.assign_driver(driver)
            self.available_drivers.remove(driver)
            return True
        
        return False
    
    def start_ride(self, ride_id: str) -> bool:
        """Start a ride (driver en route to pickup)"""
        if ride_id in self.active_rides:
            ride = self.active_rides[ride_id]
            return ride.start_ride()
        return False
    
    def pickup_rider(self, ride_id: str) -> bool:
        """Driver has picked up the rider"""
        if ride_id in self.active_rides:
            ride = self.active_rides[ride_id]
            return ride.pickup_rider()
        return False
    
    def complete_ride(self, ride_id: str) -> bool:
        """Complete a ride and calculate fare"""
        if ride_id in self.active_rides:
            ride = self.active_rides[ride_id]
            
            # Calculate fare
            ride.fare = self.pricing_strategy.calculate_fare(ride)
            
            # Complete the ride
            success = ride.complete_ride()
            
            if success:
                # Add driver back to available pool
                if ride.driver and ride.driver.is_available:
                    self.available_drivers.append(ride.driver)
                
                # Remove from active rides
                del self.active_rides[ride_id]
            
            return success
        
        return False
    
    def cancel_ride(self, ride_id: str) -> bool:
        """Cancel a ride"""
        if ride_id in self.active_rides:
            ride = self.active_rides[ride_id]
            success = ride.cancel_ride()
            
            if success:
                # Add driver back to available pool if there was one
                if ride.driver and ride.driver.is_available:
                    self.available_drivers.append(ride.driver)
                
                # Remove from active rides
                del self.active_rides[ride_id]
            
            return success
        
        return False
    
    def get_ride(self, ride_id: str) -> Optional[Ride]:
        """Get a ride by ID"""
        return self.rides.get(ride_id)
    
    def get_active_rides(self) -> List[Ride]:
        """Get all active rides"""
        return list(self.active_rides.values())
    
    def get_available_drivers(self) -> List[Driver]:
        """Get all available drivers"""
        return self.available_drivers 