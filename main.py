from managers.user_manager import UserManager
from managers.ride_manager import RideManager
from models.ride import VehicleType
from strategies.driver_matching import NearestDriverStrategy, HighestRatedDriverStrategy
from strategies.pricing import BasePricingStrategy, SurgePricingDecorator, DiscountDecorator
import time

def main():
    """Main function to demonstrate the ride-sharing platform"""
    print("=== Ride-Sharing Service Platform Demo ===\n")
    
    # Get singleton instances
    user_manager = UserManager()
    ride_manager = RideManager()
    
    # Register some riders
    print("Registering riders...")
    alice = user_manager.register_rider("Alice", "123-456-7890", (0.0, 0.0))
    bob = user_manager.register_rider("Bob", "234-567-8901", (5.0, 5.0))
    charlie = user_manager.register_rider("Charlie", "345-678-9012", (10.0, 10.0))
    print(f"Registered {len(user_manager.get_all_riders())} riders\n")
    
    # Register some drivers
    print("Registering drivers...") # name , phone_no , car_id , car name , vehicle type , capacity , coordinate
    driver1 = user_manager.register_driver("Dave", "456-789-0123", "CAR001", "Toyota Camry", 
                                         VehicleType.SEDAN.value, 4, (1.0, 1.0))
    driver2 = user_manager.register_driver("Eve", "567-890-1234", "CAR002", "Honda Civic", 
                                         VehicleType.SEDAN.value, 4, (6.0, 6.0))
    driver3 = user_manager.register_driver("Frank", "678-901-2345", "CAR003", "Ford Explorer", 
                                         VehicleType.SUV.value, 6, (11.0, 11.0))
    driver4 = user_manager.register_driver("Grace", "789-012-3456", "BIKE001", "Honda CBR", 
                                         VehicleType.BIKE.value, 1, (3.0, 3.0))
    print(f"Registered {len(user_manager.get_all_drivers())} drivers\n")
    
    # Register drivers with ride manager
    for driver in user_manager.get_all_drivers():
        ride_manager.register_driver(driver)
    print(f"Available drivers: {len(ride_manager.get_available_drivers())}\n")
    
    # Demo 1: Regular ride with nearest driver strategy
    print("=== Demo 1: Regular Ride with Nearest Driver Strategy ===")
    ride_manager.set_driver_matching_strategy(NearestDriverStrategy())
    ride_manager.set_pricing_strategy(BasePricingStrategy())
    
    print("Alice is requesting a ride...")
    ride1 = ride_manager.request_ride(alice, (0.0, 0.0), (10.0, 10.0), VehicleType.SEDAN)
    print(f"Ride ID: {ride1.id}")
    
    print("\nSimulating ride flow...")
    time.sleep(1)  # Simulate time passing
    
    ride_manager.start_ride(ride1.id)
    time.sleep(1)  # Simulate time passing
    
    ride_manager.pickup_rider(ride1.id)
    time.sleep(1)  # Simulate time passing
    
    ride_manager.complete_ride(ride1.id)
    print(f"Ride completed. Fare: ${ride1.fare:.2f}\n")
    
    # Demo 2: Carpool ride with highest rated driver strategy
    print("=== Demo 2: Carpool Ride with Highest Rated Driver Strategy ===")
    ride_manager.set_driver_matching_strategy(HighestRatedDriverStrategy())
    
    # Apply surge pricing decorator
    base_pricing = BasePricingStrategy()
    surge_pricing = SurgePricingDecorator(base_pricing, 1.5)
    ride_manager.set_pricing_strategy(surge_pricing)
    
    print("Bob is requesting a carpool ride...")
    ride2 = ride_manager.request_carpool(bob, (5.0, 5.0), (15.0, 15.0), VehicleType.SUV)
    print(f"Ride ID: {ride2.id}")
    
    print("\nSimulating ride flow...")
    time.sleep(1)  # Simulate time passing
    
    ride_manager.start_ride(ride2.id)
    time.sleep(1)  # Simulate time passing
    
    ride_manager.pickup_rider(ride2.id)
    time.sleep(1)  # Simulate time passing
    
    ride_manager.complete_ride(ride2.id)
    print(f"Ride completed. Fare with surge pricing: ${ride2.fare:.2f}\n")
    
    # Demo 3: Regular ride with discount
    print("=== Demo 3: Regular Ride with Discount ===")
    ride_manager.set_driver_matching_strategy(NearestDriverStrategy())
    
    # Apply discount decorator
    base_pricing = BasePricingStrategy()
    discount_pricing = DiscountDecorator(base_pricing, 15.0)  # 15% discount
    ride_manager.set_pricing_strategy(discount_pricing)
    
    print("Charlie is requesting a ride...")
    ride3 = ride_manager.request_ride(charlie, (10.0, 10.0), (0.0, 0.0), VehicleType.BIKE)
    print(f"Ride ID: {ride3.id}")
    
    print("\nSimulating ride flow...")
    time.sleep(1)  # Simulate time passing
    
    ride_manager.start_ride(ride3.id)
    time.sleep(1)  # Simulate time passing
    
    ride_manager.pickup_rider(ride3.id)
    time.sleep(1)  # Simulate time passing
    
    ride_manager.complete_ride(ride3.id)
    print(f"Ride completed. Fare with discount: ${ride3.fare:.2f}\n")
    
    # Summary
    print("=== Summary ===")
    print(f"Total rides: {len(ride_manager.rides)}")
    print(f"Active rides: {len(ride_manager.active_rides)}")
    print(f"Available drivers: {len(ride_manager.available_drivers)}")

if __name__ == "__main__":
    main() 