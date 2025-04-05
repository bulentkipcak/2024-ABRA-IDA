"""
AbraIda Class for MAVLink Vehicle Control
Author: Bülent Kıpçak
Date: 05-04-2025
Version: 1.1
Description: This class provides methods for connecting to a MAVLink-compatible vehicle,
retrieving its current state, setting yaw and velocity targets, and handling JSON files
for vehicle mode and state information.
"""

import math
import json
from pymavlink import mavutil

class AbraIda:
    def __init__(self, connection_string):
        self.master = mavutil.mavlink_connection(connection_string)
        self.master.wait_heartbeat()
        print("Araca bağlandı.")

    def get_current_vehicle_mode(self):
        msg = self.master.recv_match(type='HEARTBEAT', blocking=True)
        if msg:
            return mavutil.mode_string_v10(msg)
        return None

    def get_current_yaw(self):
        msg = self.master.recv_match(type='ATTITUDE', blocking=True)
        return math.degrees(msg.yaw)

    def set_yaw_target(self, yaw_angle):
        yaw_radians = math.radians(yaw_angle)
        msg = self.master.mav.set_position_target_local_ned_encode(
            0, 1, 1, mavutil.mavlink.MAV_FRAME_LOCAL_NED, 0b100111111111, 0, 0, 0, 0, 0, 0, 0, 0, yaw_radians, 0
        )
        self.master.mav.send(msg)

    def set_velocity_target(self, forward_velocity):
        msg = self.master.mav.set_position_target_local_ned_encode(
            0, 1, 1, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 0b110111100111, 0, 0, 0, forward_velocity, 0, 0, 0, 0, 0, 0
        )
        self.master.mav.send(msg)

    def read_error_yaw_from_json(self, filename='error_angle.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return data['error_yaw']
        except Exception as e:
            print(f"Error reading yaw from json: {e}")
            return None

    def read_vehicle_state(self, filename='vehicle_state.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return data['vehicle_state']
        except Exception as e:
            print(f"Error reading vehicle state: {e}")
            return None

    def update_json_mode(self, mode, filename='vehicle_mode.json'):
        data = {'vehicle_mode': mode}
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
