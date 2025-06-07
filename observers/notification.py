from abc import ABC, abstractmethod
from models.ride import Ride, RideStatus

class Observer(ABC):
    """Abstract observer interface"""
    
    @abstractmethod
    def update(self, ride: Ride):
        """Update method called when observed subject changes"""
        pass

class RiderNotificationObserver(Observer):
    """Observer that sends notifications to the rider"""
    
    def update(self, ride: Ride):
        """Send notification to rider based on ride status"""
        if ride.status == RideStatus.DRIVER_ASSIGNED:
            self._notify_driver_assigned(ride)
        elif ride.status == RideStatus.DRIVER_EN_ROUTE:
            self._notify_driver_en_route(ride)
        elif ride.status == RideStatus.RIDE_IN_PROGRESS:
            self._notify_ride_started(ride)
        elif ride.status == RideStatus.COMPLETED:
            self._notify_ride_completed(ride)
        elif ride.status == RideStatus.CANCELLED:
            self._notify_ride_cancelled(ride)
    
    def _notify_driver_assigned(self, ride: Ride):
        message = f"Rider Notification: Driver {ride.driver.name} has been assigned to your ride. " \
                 f"Vehicle: {ride.driver.vehicle.model} ({ride.driver.vehicle.vehicle_id})"
        print(message)
    
    def _notify_driver_en_route(self, ride: Ride):
        message = f"Rider Notification: Driver {ride.driver.name} is on the way to pick you up."
        print(message)
    
    def _notify_ride_started(self, ride: Ride):
        message = f"Rider Notification: Your ride has started. Enjoy your trip!"
        print(message)
    
    def _notify_ride_completed(self, ride: Ride):
        message = f"Rider Notification: Your ride has been completed. Fare: ${ride.fare:.2f}"
        print(message)
    
    def _notify_ride_cancelled(self, ride: Ride):
        message = f"Rider Notification: Your ride has been cancelled."
        print(message)

class DriverNotificationObserver(Observer):
    """Observer that sends notifications to the driver"""
    
    def update(self, ride: Ride):
        """Send notification to driver based on ride status"""
        if not ride.driver:
            return
            
        if ride.status == RideStatus.DRIVER_ASSIGNED:
            self._notify_ride_assigned(ride)
        elif ride.status == RideStatus.DRIVER_EN_ROUTE:
            self._notify_pickup_instructions(ride)
        elif ride.status == RideStatus.RIDE_IN_PROGRESS:
            self._notify_ride_started(ride)
        elif ride.status == RideStatus.COMPLETED:
            self._notify_ride_completed(ride)
        elif ride.status == RideStatus.CANCELLED:
            self._notify_ride_cancelled(ride)
    
    def _notify_ride_assigned(self, ride: Ride):
        message = f"Driver Notification: You have been assigned a new ride. " \
                 f"Pickup location: {ride.pickup_location}"
        print(message)
    
    def _notify_pickup_instructions(self, ride: Ride):
        message = f"Driver Notification: Please proceed to pickup location at {ride.pickup_location} " \
                 f"to pick up {ride.rider.name}."
        print(message)
    
    def _notify_ride_started(self, ride: Ride):
        message = f"Driver Notification: Ride started. Navigate to {ride.dropoff_location}"
        print(message)
    
    def _notify_ride_completed(self, ride: Ride):
        message = f"Driver Notification: Ride completed. Earned: ${ride.fare:.2f}"
        print(message)
    
    def _notify_ride_cancelled(self, ride: Ride):
        message = f"Driver Notification: Ride has been cancelled."
        print(message)

class SystemLogObserver(Observer):
    """Observer that logs all ride events to the system"""
    
    def update(self, ride: Ride):
        """Log ride status changes"""
        print(f"System Log: Ride {ride.id} status changed to {ride.status.value}")
        
        if ride.status == RideStatus.COMPLETED:
            print(f"System Log: Ride completed. Distance: {ride.distance:.2f} km, Fare: ${ride.fare:.2f}") 