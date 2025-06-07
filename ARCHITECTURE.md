# Ride-Sharing Platform Architecture

This document describes the architecture of the ride-sharing platform, highlighting the design patterns and SOLID principles used.

## Class Diagram (UML)

```
+-------------------+     +-------------------+     +-------------------+
|      User         |     |      Ride         |     |   RideManager     |
+-------------------+     +-------------------+     +-------------------+
| - id: str         |     | - id: str         |     | - rides: Dict     |
| - name: str       |     | - rider: Rider    |     | - active_rides    |
| - phone: str      |     | - driver: Driver  |     | - avail_drivers   |
+-------------------+     | - pickup_location |     +-------------------+
        ^                 | - dropoff_location|     | + request_ride()  |
        |                 | - status          |     | + complete_ride() |
+-------+-------+         | - observers       |     | + cancel_ride()   |
|               |         +-------------------+     +-------------------+
|               |         | + assign_driver() |             ^
+-------+       +-------+ | + start_ride()    |             | Singleton
|  Rider |      | Driver | | + complete_ride() |            |
+-------+       +-------+ +-------------------+     +-------------------+
| - location    | - vehicle|        ^                |   UserManager    |
| - history     | - rating |        |                +-------------------+
+---------------+---------+         |                | - riders: Dict    |
                                    |                | - drivers: Dict   |
                                    |                +-------------------+
                          +---------+---------+      | + register_rider()|
                          |                   |      | + register_driver()|
                  +-------+-------+   +-------+-----+-------------------+
                  | RegularRide   |   | CarpoolRide |
                  +---------------+   +-------------+


+----------------------+     +----------------------+
| DriverMatchingStrategy|     |   PricingStrategy   |
+----------------------+     +----------------------+
| + find_driver()      |     | + calculate_fare()   |
+----------------------+     +----------------------+
        ^                              ^
        |                              |
+-------+--------+           +---------+--------+
|                |           |                  |
+-------+  +-----+----+      +--------+  +-----+----+
|Nearest |  |Highest   |      |Base    |  |Pricing   |
|Driver  |  |Rated     |      |Pricing |  |Decorator |
|Strategy|  |Strategy  |      |Strategy|  |          |
+--------+  +----------+      +--------+  +----------+
                                               ^
                                               |
                                      +--------+--------+
                                      |                 |
                               +------+------+  +-------+-----+
                               |Surge        |  |Discount     |
                               |Pricing      |  |Decorator    |
                               |Decorator    |  |             |
                               +-------------+  +-------------+


+------------------+     +---------------------+
|    Observer      |     |    RideFactory      |
+------------------+     +---------------------+
| + update()       |     | + create_regular()  |
+------------------+     | + create_carpool()  |
        ^                +---------------------+
        |
+-------+--------+
|                |
+-------+  +-----+------------+  +------------+
|Rider   |  |Driver           |  |System      |
|Notifier|  |Notifier         |  |Logger      |
+--------+  +----------------+   +------------+
```

## Design Patterns Used

### 1. Strategy Pattern

- **Driver Matching Strategy**: Allows different algorithms for matching drivers to rides

  - `NearestDriverStrategy`: Matches the nearest available driver
  - `HighestRatedDriverStrategy`: Matches the highest rated available driver

- **Pricing Strategy**: Allows different algorithms for calculating ride fares
  - `BasePricingStrategy`: Basic fare calculation based on distance and vehicle type

### 2. Decorator Pattern

- **Pricing Decorators**: Add additional behaviors to pricing strategies
  - `SurgePricingDecorator`: Applies a surge multiplier to the fare
  - `DiscountDecorator`: Applies a discount to the fare

### 3. Observer Pattern

- **Ride Observers**: Get notified when ride status changes
  - `RiderNotificationObserver`: Sends notifications to the rider
  - `DriverNotificationObserver`: Sends notifications to the driver
  - `SystemLogObserver`: Logs ride events

### 4. Factory Pattern

- **Ride Factory**: Creates different types of rides
  - `create_regular_ride()`: Creates a regular ride
  - `create_carpool_ride()`: Creates a carpool ride

### 5. Singleton Pattern

- **RideManager**: Single instance that manages all rides
- **UserManager**: Single instance that manages all users

## SOLID Principles

### 1. Single Responsibility Principle

Each class has a single responsibility:

- `Ride`: Manages ride state and lifecycle
- `Driver`: Manages driver-specific attributes and behaviors
- `Rider`: Manages rider-specific attributes and behaviors
- `RideManager`: Orchestrates ride operations
- `UserManager`: Manages user registration and retrieval

### 2. Open/Closed Principle

The system is open for extension but closed for modification:

- New driver matching strategies can be added without modifying existing code
- New pricing strategies and decorators can be added without modifying existing code
- New ride types can be added without modifying existing code

### 3. Liskov Substitution Principle

Subtypes can be substituted for their base types:

- `Driver` and `Rider` can be used wherever `User` is expected
- Different driver matching strategies can be used interchangeably
- Different pricing strategies can be used interchangeably

### 4. Interface Segregation Principle

Interfaces are specific to client needs:

- `Observer` interface has only the methods needed by observers
- `DriverMatchingStrategy` interface has only the methods needed for matching drivers

### 5. Dependency Inversion Principle

High-level modules depend on abstractions, not details:

- `RideManager` depends on the `DriverMatchingStrategy` interface, not concrete implementations
- `RideManager` depends on the `PricingStrategy` interface, not concrete implementations
- `Ride` depends on the `Observer` interface, not concrete implementations
