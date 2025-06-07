# Ride-Sharing Platform Implementation Summary

## Overview

This project implements an in-memory, object-oriented ride-sharing service platform that demonstrates clean Low-Level Design (LLD) using SOLID principles and multiple design patterns. The platform enables riders to book rides and get matched with drivers in a simulated environment.

## Key Features

1. **User Management**: Registration and management of Riders and Drivers
2. **Ride Booking**: Riders can request rides with pickup and dropoff locations
3. **Driver Matching**: Multiple algorithms for matching drivers to rides
4. **Ride Workflow**: Complete ride lifecycle from booking to completion
5. **Vehicle/Ride Types**: Support for multiple vehicle types and ride options
6. **Pricing Strategies**: Flexible fare calculation with modifiers
7. **Notifications**: Event-based notification system

## Design Patterns Implemented

### 1. Strategy Pattern

Used for implementing interchangeable algorithms:

- **Driver Matching Strategies**:

  - `NearestDriverStrategy`: Matches the nearest available driver to the rider
  - `HighestRatedDriverStrategy`: Matches the highest-rated available driver

- **Pricing Strategies**:
  - `BasePricingStrategy`: Calculates fare based on distance and vehicle type

### 2. Decorator Pattern

Used to add additional behaviors to pricing:

- `PricingDecorator`: Base decorator for pricing strategies
- `SurgePricingDecorator`: Applies surge pricing multiplier
- `DiscountDecorator`: Applies discount percentage

### 3. Observer Pattern

Used for notifications when ride status changes:

- `RiderNotificationObserver`: Sends notifications to the rider
- `DriverNotificationObserver`: Sends notifications to the driver
- `SystemLogObserver`: Logs system events

### 4. Factory Pattern

Used for creating different types of rides:

- `RideFactory`: Creates regular and carpool rides with appropriate validation

### 5. Singleton Pattern

Used for manager classes that orchestrate core functions:

- `RideManager`: Single instance that manages all rides
- `UserManager`: Single instance that manages all users

## SOLID Principles Applied

1. **Single Responsibility Principle**:

   - Each class has a well-defined responsibility
   - Clear separation between models, strategies, managers, and observers

2. **Open/Closed Principle**:

   - New strategies can be added without modifying existing code
   - New ride types can be added without changing core logic

3. **Liskov Substitution Principle**:

   - Subtypes can be used wherever base types are expected
   - Different strategies can be substituted without affecting functionality

4. **Interface Segregation Principle**:

   - Interfaces are specific to client needs
   - No client is forced to depend on methods it doesn't use

5. **Dependency Inversion Principle**:
   - High-level modules depend on abstractions
   - Implementation details depend on abstractions

## Extensibility

The design allows for easy extension in multiple ways:

- New driver matching algorithms can be added by implementing the `DriverMatchingStrategy` interface
- New pricing strategies can be added by implementing the `PricingStrategy` interface
- New pricing modifiers can be added by extending the `PricingDecorator` class
- New ride types can be added by extending the `Ride` class and adding factory methods
- New notification types can be added by implementing the `Observer` interface

## Demo Scenarios

The main.py file demonstrates three scenarios:

1. Regular ride with nearest driver strategy and base pricing
2. Carpool ride with highest-rated driver strategy and surge pricing
3. Regular ride with nearest driver strategy and discount pricing

Each scenario shows the complete lifecycle of a ride from request to completion, including notifications at each step.
