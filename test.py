import unittest
from models.user import Rider, Driver, Vehicle
from models.ride import Ride, VehicleType, RideStatus
from strategies.driver_matching import NearestDriverStrategy, HighestRatedDriverStrategy
from strategies.pricing import BasePricingStrategy, SurgePricingDecorator, DiscountDecorator
from managers.ride_manager import RideManager
from managers.user_manager import UserManager
from factories.ride_factory import RideFactory

class TestRideSharingPlatform(unittest.TestCase):
    
    def setUp(self):
        # Reset singletons for testing
        RideManager._instance = None
        UserManager._instance = None
        
        self.user_manager = UserManager()
        self.ride_manager = RideManager()
        
        # Create test riders with proper lat/lon coordinates
        # Central coordinates (New York City area as an example)
        self.rider1 = self.user_manager.register_rider("Test Rider 1", "111-111-1111", (40.7128, -74.0060))
        self.rider2 = self.user_manager.register_rider("Test Rider 2", "222-222-2222", (40.7300, -73.9950))
        
        # Create test drivers within 10km of the riders
        # Driver1 is about 3km from rider1
        self.driver1 = self.user_manager.register_driver("Test Driver 1", "333-333-3333", 
                                                      "TEST001", "Test Car 1", 
                                                      VehicleType.SEDAN.value, 4, (40.7400, -74.0080))
        # Driver2 is about 5km from rider1
        self.driver2 = self.user_manager.register_driver("Test Driver 2", "444-444-4444", 
                                                      "TEST002", "Test Car 2", 
                                                      VehicleType.SUV.value, 6, (40.7600, -73.9800))
        
        # Register drivers with ride manager
        self.ride_manager.register_driver(self.driver1)
        self.ride_manager.register_driver(self.driver2)
        
        # Standard pickup and dropoff locations for tests
        self.pickup_location = (40.7128, -74.0060)  # NYC
        self.dropoff_location = (40.8000, -73.9000)  # About 10km away
    
    def test_rider_registration(self):
        """Test that riders can be registered and retrieved"""
        self.assertEqual(len(self.user_manager.get_all_riders()), 2)
        self.assertEqual(self.user_manager.get_rider(self.rider1.id).name, "Test Rider 1")
    
    def test_driver_registration(self):
        """Test that drivers can be registered and retrieved"""
        self.assertEqual(len(self.user_manager.get_all_drivers()), 2)
        self.assertEqual(self.user_manager.get_driver(self.driver1.id).name, "Test Driver 1")
    
    def test_ride_request_with_nearest_driver(self):
        """Test ride request with nearest driver strategy"""
        self.ride_manager.set_driver_matching_strategy(NearestDriverStrategy())
        
        ride = self.ride_manager.request_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.SEDAN)
        
        self.assertIsNotNone(ride)
        self.assertEqual(ride.status, RideStatus.DRIVER_ASSIGNED)
        self.assertEqual(ride.driver.id, self.driver1.id)  # Should match nearest driver (driver1)
    
    def test_ride_request_with_highest_rated_driver(self):
        """Test ride request with highest rated driver strategy"""
        # Set driver2 with higher rating
        self.driver2.rating = 5.0
        self.driver1.rating = 4.0
        
        self.ride_manager.set_driver_matching_strategy(HighestRatedDriverStrategy())
        
        ride = self.ride_manager.request_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.SEDAN)
        
        self.assertIsNotNone(ride)
        self.assertEqual(ride.status, RideStatus.DRIVER_ASSIGNED)
        self.assertEqual(ride.driver.id, self.driver1.id)  # Should match highest rated driver with correct vehicle type
    
    def test_ride_lifecycle(self):
        """Test the complete lifecycle of a ride"""
        ride = self.ride_manager.request_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.SEDAN)
        ride_id = ride.id
        
        # Start ride
        self.assertTrue(self.ride_manager.start_ride(ride_id))
        self.assertEqual(ride.status, RideStatus.DRIVER_EN_ROUTE)
        
        # Pickup rider
        self.assertTrue(self.ride_manager.pickup_rider(ride_id))
        self.assertEqual(ride.status, RideStatus.RIDE_IN_PROGRESS)
        
        # Complete ride
        self.assertTrue(self.ride_manager.complete_ride(ride_id))
        self.assertEqual(ride.status, RideStatus.COMPLETED)
        self.assertGreater(ride.fare, 0)
    
    def test_pricing_strategies(self):
        """Test different pricing strategies"""
        # Use the same route and rider for all pricing tests to ensure fair comparison
        
        # Base pricing
        self.ride_manager.set_pricing_strategy(BasePricingStrategy())
        ride1 = self.ride_manager.request_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.SEDAN)
        self.ride_manager.complete_ride(ride1.id)
        base_fare = ride1.fare
        
        # Reset ride manager to ensure clean state
        RideManager._instance = None
        self.ride_manager = RideManager()
        self.ride_manager.register_driver(self.driver1)
        
        # Surge pricing (1.5x)
        base_strategy = BasePricingStrategy()
        surge_strategy = SurgePricingDecorator(base_strategy, 1.5)
        self.ride_manager.set_pricing_strategy(surge_strategy)
        ride2 = self.ride_manager.request_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.SEDAN)
        self.ride_manager.complete_ride(ride2.id)
        surge_fare = ride2.fare
        
        # Reset ride manager again
        RideManager._instance = None
        self.ride_manager = RideManager()
        self.ride_manager.register_driver(self.driver1)
        
        # Discount pricing (10% off)
        discount_strategy = DiscountDecorator(BasePricingStrategy(), 10.0)
        self.ride_manager.set_pricing_strategy(discount_strategy)
        ride3 = self.ride_manager.request_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.SEDAN)
        self.ride_manager.complete_ride(ride3.id)
        discount_fare = ride3.fare
        
        # Verify that surge pricing increases the fare and discount reduces it
        self.assertAlmostEqual(surge_fare / base_fare, 1.5, places=1)
        self.assertAlmostEqual(discount_fare / base_fare, 0.9, places=1)
    
    def test_ride_factory(self):
        """Test the ride factory creates appropriate ride types"""
        regular_ride = RideFactory.create_regular_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.SEDAN)
        carpool_ride = RideFactory.create_carpool_ride(self.rider2, self.pickup_location, self.dropoff_location, VehicleType.SUV)
        
        self.assertEqual(regular_ride.ride_type.value, "REGULAR")
        self.assertEqual(carpool_ride.ride_type.value, "CARPOOL")
        
        # Test that carpool rides enforce appropriate vehicle types
        bike_carpool = RideFactory.create_carpool_ride(self.rider1, self.pickup_location, self.dropoff_location, VehicleType.BIKE)
        self.assertEqual(bike_carpool.vehicle_type, VehicleType.SEDAN)  # Should default to sedan

if __name__ == '__main__':
    unittest.main() 