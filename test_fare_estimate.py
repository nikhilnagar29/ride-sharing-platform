import requests
import json

# API base URL
base_url = "http://localhost:8000/api/rides/estimate"

# Test cases for different pricing strategies and vehicle types
test_cases = [
    {
        "name": "Base pricing - Sedan",
        "request": {
            "pickup_location": [40.7128, -74.0060],  # New York
            "dropoff_location": [40.7484, -73.9857],  # Empire State Building
            "vehicle_type": "SEDAN",
            "pricing_strategy": "BASE"
        }
    },
    {
        "name": "Surge pricing - SUV",
        "request": {
            "pickup_location": [40.7128, -74.0060],  # New York
            "dropoff_location": [40.7484, -73.9857],  # Empire State Building
            "vehicle_type": "SUV",
            "pricing_strategy": "SURGE",
            "surge_multiplier": 1.5
        }
    },
    {
        "name": "Discount pricing - Bike",
        "request": {
            "pickup_location": [40.7128, -74.0060],  # New York
            "dropoff_location": [40.7484, -73.9857],  # Empire State Building
            "vehicle_type": "BIKE",
            "pricing_strategy": "DISCOUNT",
            "discount_percentage": 10.0
        }
    }
]

# Run the tests
for test in test_cases:
    print(f"\nTesting: {test['name']}")
    
    try:
        # Make the request
        response = requests.post(base_url, json=test["request"])
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            print(f"Estimated fare: ${result['estimated_fare']:.2f}")
            print(f"Distance: {result['distance']:.2f} km")
            print(f"Vehicle type: {result['vehicle_type']}")
            print(f"Pricing strategy: {result['pricing_strategy']}")
            print(f"Base fare: ${result['base_fare']:.2f}")
            print(f"Per km rate: ${result['per_km_rate']:.2f}")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
    
    except Exception as e:
        print(f"Exception: {str(e)}")

print("\nAll tests completed.") 