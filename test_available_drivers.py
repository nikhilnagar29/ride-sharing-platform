import requests
import json

# API base URL
base_url = "http://localhost:8000/api/drivers/available"

# Test cases for finding available drivers
test_cases = [
    {
        "name": "All available drivers within 15km",
        "request": {
            "location": [40.7128, -74.0060],  # New York
            "max_distance": 15.0
        }
    },
    {
        "name": "Available SEDAN drivers within 15km",
        "request": {
            "location": [40.7128, -74.0060],  # New York
            "max_distance": 15.0,
            "vehicle_type": "SEDAN"
        }
    },
    {
        "name": "Available drivers within 5km",
        "request": {
            "location": [40.7128, -74.0060],  # New York
            "max_distance": 5.0
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
            drivers = response.json()
            print(f"Found {len(drivers)} drivers")
            
            # Print details of each driver
            for i, driver in enumerate(drivers, 1):
                print(f"\nDriver {i}:")
                print(f"ID: {driver['id']}")
                print(f"Name: {driver['name']}")
                print(f"Vehicle: {driver['vehicle_model']} ({driver['vehicle_type']})")
                print(f"Vehicle ID: {driver['vehicle_id']}")
                print(f"Rating: {driver['rating']}")
                print(f"Distance: {driver['distance']:.2f} km")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
    
    except Exception as e:
        print(f"Exception: {str(e)}")

print("\nAll tests completed.") 