"""
Main script for controlling the maritime vehicle using MAVLink protocol.
Author: Bülent Kıpçak
Date: 05-04-2025
Version: 1.1
Description: This script initializes the connection to the vehicle and manages vehicle state
through the VehicleStateHandler. It runs data updating and vehicle control in separate threads.
"""

from abra_ida import AbraIda
from states import VehicleStateHandler
import time
import threading

# connection_string = "tcp:192.168.31.60:5760"
connection_string = "tcp:127.0.0.1:5762"
vehicle = AbraIda(connection_string)
state_handler = VehicleStateHandler(vehicle)

def data_updater():
    global vehicle_mode, error_yaw, vehicle_state, current_yaw

    while True:
        vehicle_mode = vehicle.get_current_vehicle_mode()
        error_yaw = vehicle.read_error_yaw_from_json()
        vehicle_state = vehicle.read_vehicle_state()
        current_yaw = vehicle.get_current_yaw()
        time.sleep(0.2)

def vehicle_controller():
    while True:
        if error_yaw is None or vehicle_state is None:
            time.sleep(0.1)
            continue

        state_handler.set_state(vehicle_state)
        state_handler.handle(current_yaw, error_yaw)
        time.sleep(0.5)

if __name__ == "__main__":
    data_thread = threading.Thread(target=data_updater, daemon=True)
    control_thread = threading.Thread(target=vehicle_controller, daemon=True)

    data_thread.start()
    control_thread.start()

    try:
        while True:
            time.sleep(1)  
    except KeyboardInterrupt:
        print("Program sonlandırılıyor...")
