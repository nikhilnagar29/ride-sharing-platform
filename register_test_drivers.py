import requests
import json
import random

# API base URL
base_url = "http://localhost:8000/api"

# Sample driver data
drivers = [
    {
        "name": "Dave Smith",
        "phone": "456-789-0123",
        "vehicle": {
            "vehicle_id": "CAR001",
            "model": "Toyota Camry",
            "vehicle_type": "SEDAN",
            "capacity": 4
        },
        "current_location": [40.7128, -74.0060]  # New York
    },
    {
        "name": "Eve Johnson",
        "phone": "567-890-1234",
        "vehicle": {
            "vehicle_id": "CAR002",
            "model": "Honda Civic",
            "vehicle_type": "SEDAN",
            "capacity": 4
        },
        "current_location": [40.7214, -73.9896]  # 2km from New York
    },
    {
        "name": "Frank Williams",
        "phone": "678-901-2345",
        "vehicle": {
            "vehicle_id": "CAR003",
            "model": "Ford Explorer",
            "vehicle_type": "SUV",
            "capacity": 6
        },
        "current_location": [40.7306, -74.0210]  # 3km from New York
    },
    {
        "name": "Grace Brown",
        "phone": "789-012-3456",
        "vehicle": {
            "vehicle_id": "BIKE001",
            "model": "Honda CBR",
            "vehicle_type": "BIKE",
            "capacity": 1
        },
        "current_location": [40.7589, -73.9851]  # 6km from New York
    },
    {
        "name": "Henry Davis",
        "phone": "890-123-4567",
        "vehicle": {
            "vehicle_id": "CAR004",
            "model": "Chevrolet Suburban",
            "vehicle_type": "SUV",
            "capacity": 7
        },
        "current_location": [40.7829, -73.9654]  # 9km from New York
    },
    {
        "name": "Irene Miller",
        "phone": "901-234-5678",
        "vehicle": {
            "vehicle_id": "AUTO001",
            "model": "Bajaj RE",
            "vehicle_type": "AUTO_RICKSHAW",
            "capacity": 3
        },
        "current_location": [40.8075, -74.0919]  # 12km from New York
    },
    {
        "name": "Jack Wilson",
        "phone": "012-345-6789",
        "vehicle": {
            "vehicle_id": "CAR005",
            "model": "Tesla Model 3",
            "vehicle_type": "SEDAN",
            "capacity": 4
        },
        "current_location": [40.8554, -73.9239]  # 18km from New York
    }
]

# Register drivers
print("Registering drivers...")
registered_drivers = []

for driver in drivers:
    try:
        # Register the driver
        response = requests.post(f"{base_url}/drivers/", json=driver)
        
        if response.status_code == 200:
            driver_data = response.json()
            registered_drivers.append(driver_data)
            print(f"Registered driver: {driver_data['name']} with ID: {driver_data['id']}")
            
            # Set driver as available
            availability_response = requests.put(
                f"{base_url}/drivers/{driver_data['id']}/availability",
                json={"is_available": True}
            )
            
            if availability_response.status_code == 200:
                print(f"Set {driver_data['name']} as available")
            else:
                print(f"Failed to set availability: {availability_response.status_code}")
                print(availability_response.json())
        else:
            print(f"Failed to register driver: {response.status_code}")
            print(response.json())
    
    except Exception as e:
        print(f"Exception: {str(e)}")

print(f"\nRegistered {len(registered_drivers)} drivers")
print("Done!") 