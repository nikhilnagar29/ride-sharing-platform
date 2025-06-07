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

## Design Patterns Used

- Strategy Pattern: For driver matching algorithms and pricing strategies
- Factory Pattern: For creating different types of rides and vehicles
- Singleton Pattern: For manager classes that orchestrate core functions
- Observer Pattern: For notifications when ride status changes
- Decorator Pattern: For adding additional behaviors to fare calculation

## How to Run

```
python main.py
```
# ride-sharing-platform
