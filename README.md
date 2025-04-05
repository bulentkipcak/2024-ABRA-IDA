# 2024 ABRA IDA
 This project implements a ship control system using Pymavlink. It leverages computer vision to detect buoys and control the ship's movements based on the detected objects. The main components of the project include a detector for identifying colored buoys and a control library for managing the ship's operations.

## File Descriptions

- **`main.py`**  
  This is the main entry point of the application. It initializes the system, starts the detection process, and manages the ship's control commands based on the detections.

- **`detector.py`**  
  Contains the logic for detecting buoys of different colors (red, yellow, green) using OpenCV. It defines a `Buoy` class to store coordinates and IDs of detected buoys, and processes frames to identify colored markers for navigation decisions.

- **`abra_ida.py`**  
  This library is responsible for interfacing with the MAVLink protocol. It reads and writes mission-critical data from JSON files to track the ship’s current mode and status. It also includes functions for sending control commands to the ship, such as velocity and yaw targets.

- **`states.py`**  
  Implements the State Pattern to manage the vehicle's various operational modes. Each state is defined as a subclass of `VehicleState` and encapsulates specific behaviors like turning, aligning, or moving forward. The `VehicleStateHandler` class controls transitions between states based on contextual cues, offering clean and maintainable navigation logic.

## Dependencies

- Threading
- OpenCV
- Pymavlink
- NumPy

