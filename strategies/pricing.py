from abc import ABC, abstractmethod
from models.ride import Ride, VehicleType

class PricingStrategy(ABC):
    """Abstract strategy for calculating ride fare"""
    
    @abstractmethod
    def calculate_fare(self, ride: Ride) -> float:
        """Calculate the fare for a ride"""
        pass

class BasePricingStrategy(PricingStrategy):
    """Base pricing strategy with distance and vehicle type considerations"""
    
    def calculate_fare(self, ride: Ride) -> float:
        # Base fare by vehicle type
        base_fare = self._get_base_fare(ride.vehicle_type)
        
        # Distance-based fare
        distance_fare = ride.distance * self._get_per_km_rate(ride.vehicle_type)
        
        return base_fare + distance_fare
    
    def _get_base_fare(self, vehicle_type: VehicleType) -> float:
        """Get base fare based on vehicle type"""
        base_fares = {
            VehicleType.BIKE: 20.0,
            VehicleType.AUTO_RICKSHAW: 30.0,
            VehicleType.SEDAN: 50.0,
            VehicleType.SUV: 70.0
        }
        return base_fares.get(vehicle_type, 50.0)  # Default to SEDAN if type not found
    
    def _get_per_km_rate(self, vehicle_type: VehicleType) -> float:
        """Get per kilometer rate based on vehicle type"""
        per_km_rates = {
            VehicleType.BIKE: 5.0,
            VehicleType.AUTO_RICKSHAW: 8.0,
            VehicleType.SEDAN: 12.0,
            VehicleType.SUV: 16.0
        }
        return per_km_rates.get(vehicle_type, 12.0)  # Default to SEDAN if type not found

# Decorator pattern for pricing modifiers
class PricingDecorator(PricingStrategy):
    """Base decorator for pricing strategies"""
    
    def __init__(self, pricing_strategy: PricingStrategy):
        self.wrapped_strategy = pricing_strategy

class SurgePricingDecorator(PricingDecorator):
    """Decorator that applies surge pricing multiplier"""
    
    def __init__(self, pricing_strategy: PricingStrategy, surge_multiplier: float = 1.5):
        super().__init__(pricing_strategy)
        self.surge_multiplier = surge_multiplier
    
    def calculate_fare(self, ride: Ride) -> float:
        base_fare = self.wrapped_strategy.calculate_fare(ride)
        return base_fare * self.surge_multiplier

class DiscountDecorator(PricingDecorator):
    """Decorator that applies a discount"""
    
    def __init__(self, pricing_strategy: PricingStrategy, discount_percentage: float = 10.0):
        super().__init__(pricing_strategy)
        self.discount_percentage = discount_percentage
    
    def calculate_fare(self, ride: Ride) -> float:
        base_fare = self.wrapped_strategy.calculate_fare(ride)
        discount = (self.discount_percentage / 100) * base_fare
        return base_fare - discount 