# Ride-Sharing Platform API

This is the RESTful API for the Ride-Sharing Platform, built with FastAPI and implementing SOLID principles and various design patterns.

## Setup

1. Create a virtual environment:

   ```
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content:
   ```
   API_PORT=8000
   API_HOST=0.0.0.0
   DEBUG=True
   ```

## Running the API

Run the API server:

```
python run_api.py
```

The API will be available at:

- API: http://localhost:8000
- Interactive documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Riders

- `POST /api/riders/` - Register a new rider
- `GET /api/riders/` - Get all registered riders
- `GET /api/riders/{rider_id}` - Get a specific rider by ID
- `PUT /api/riders/{rider_id}/location` - Update a rider's current location

### Drivers

- `POST /api/drivers/` - Register a new driver
- `GET /api/drivers/` - Get all registered drivers
- `GET /api/drivers/available` - Get all available drivers
- `GET /api/drivers/{driver_id}` - Get a specific driver by ID
- `PUT /api/drivers/{driver_id}/location` - Update a driver's current location
- `PUT /api/drivers/{driver_id}/availability` - Update a driver's availability status

### Rides

- `POST /api/rides/` - Request a new ride
- `GET /api/rides/` - Get all rides
- `GET /api/rides/active` - Get all active rides
- `GET /api/rides/{ride_id}` - Get a specific ride by ID
- `PUT /api/rides/{ride_id}/start` - Start a ride (driver en route to pickup)
- `PUT /api/rides/{ride_id}/pickup` - Mark rider as picked up (ride in progress)
- `PUT /api/rides/{ride_id}/complete` - Complete a ride
- `PUT /api/rides/{ride_id}/cancel` - Cancel a ride

## Example API Requests

### Create a Rider

```bash
curl -X 'POST' \
  'http://localhost:8000/api/riders/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Doe",
  "phone": "123-456-7890",
  "default_location": [40.7128, -74.0060]
}'
```

### Create a Driver

```bash
curl -X 'POST' \
  'http://localhost:8000/api/drivers/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Jane Smith",
  "phone": "987-654-3210",
  "vehicle": {
    "vehicle_id": "ABC123",
    "model": "Toyota Camry",
    "vehicle_type": "SEDAN",
    "capacity": 4
  },
  "current_location": [40.7400, -74.0080]
}'
```

### Request a Ride

```bash
curl -X 'POST' \
  'http://localhost:8000/api/rides/' \
  -H 'Content-Type: application/json' \
  -d '{
  "rider_id": "RIDER_ID_HERE",
  "pickup_location": [40.7128, -74.0060],
  "dropoff_location": [40.8000, -73.9000],
  "vehicle_type": "SEDAN",
  "ride_type": "REGULAR",
  "driver_matching_strategy": "NEAREST",
  "pricing_strategy": "BASE"
}'
```

## Design Patterns

The API leverages the following design patterns from the core ride-sharing platform:

- **Strategy Pattern**: For driver matching algorithms and pricing strategies
- **Factory Pattern**: For creating different types of rides
- **Singleton Pattern**: For manager classes that orchestrate core functions
- **Observer Pattern**: For notifications when ride status changes
- **Decorator Pattern**: For adding additional behaviors to fare calculation

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the FastAPI application
