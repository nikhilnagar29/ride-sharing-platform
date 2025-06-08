# Ride-Sharing Service Platform

A Python-based implementation of a ride-sharing service platform that demonstrates clean Low-Level Design (LLD) using SOLID principles and multiple design patterns.

## Features

- User Management (Riders and Drivers)
- Ride Booking and Tracking
- Multiple Driver Matching Algorithms
- Different Vehicle/Ride Types
- Fare Calculation with extensible pricing strategies
- Notification System
- In-Memory Data Management
- Proper Encapsulation with Private Attributes
- RESTful API with FastAPI

## Design Patterns Used

- Strategy Pattern: For driver matching algorithms and pricing strategies
- Factory Pattern: For creating different types of rides and vehicles
- Singleton Pattern: For manager classes that orchestrate core functions
- Observer Pattern: For notifications when ride status changes
- Decorator Pattern: For adding additional behaviors to fare calculation

## Implementation Details

- Classes follow proper encapsulation principles with private attributes
- Properties (getters/setters) are used to control access to attributes
- Python conventions for privacy are followed (underscore prefix)
- See PRIVACY_IMPLEMENTATION.md for details on the privacy design

## UML Diagrams

Detailed UML diagrams are provided to visualize the system architecture:

- Class Diagram: Shows all classes, attributes, methods, and relationships
- Design Pattern Diagram: Illustrates the implementation of design patterns
- Sequence Diagram: Shows the flow of a ride booking process

See UML_DIAGRAMS.md for the diagrams and USING_UML_DIAGRAMS.md for instructions on how to use them.

## How to Run Core Application

```
python main.py
```

## How to Test

```
python test.py
```

## API

The platform also includes a RESTful API built with FastAPI:

### Setup

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

### Running the API

```
python run_api.py
```

The API will be available at:

- API: http://localhost:8000
- Interactive documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

See API_README.md for more details on available endpoints and usage examples.
