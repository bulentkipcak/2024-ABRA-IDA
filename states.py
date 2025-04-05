"""
State Pattern for Vehicle States
Author: Bülent Kıpçak
Date: 05-04-2025
Version: 1.1
Description: This file defines the state classes for different vehicle states and handles
the state transitions using the State Pattern.
"""

import time

class VehicleState:
    def handle(self, vehicle, current_yaw, error_yaw):
        raise NotImplementedError("handle() metodu alt sınıfta uygulanmalı.")

def rotate_vehicle(vehicle, angle, direction="sağa"):
    try:
        current_yaw = vehicle.get_current_yaw()
        target_yaw = current_yaw + angle
        vehicle.set_yaw_target(target_yaw)
        print(f"{direction} dönülüyor...")
    except Exception as e:
        print(f"Dönüş hatası: {e}")

class GorevYapiliyorState(VehicleState):
    def handle(self, vehicle, current_yaw, error_yaw):
        try:
            auto_pilot_error_angle = error_yaw / 4
            target_yaw = current_yaw + auto_pilot_error_angle

            print(f"Şu anki açı: {current_yaw}, Hedef açı: {target_yaw}, Fark: {current_yaw - target_yaw}")

            if abs(error_yaw) <= 5:
                print("Yaw açısı hedef farkı ±5°, 4m/s ileri hız.")
                vehicle.set_velocity_target(4)
            else:
                print("Yaw farkı ±5°'ten büyük, açı ayarlanıyor.")
                vehicle.set_yaw_target(target_yaw)
        except Exception as e:
            print(f"Görev hatası: {e}")

class KirmiziDubaState(VehicleState):
    def handle(self, vehicle, current_yaw, error_yaw):
        rotate_vehicle(vehicle, 10, "sağa")

class YesilDubaState(VehicleState):
    def handle(self, vehicle, current_yaw, error_yaw):
        rotate_vehicle(vehicle, -10, "sola")

class SariDubaState(VehicleState):
    def handle(self, vehicle, current_yaw, error_yaw):
        rotate_vehicle(vehicle, -10, "sola")
        time.sleep(5)
        rotate_vehicle(vehicle, 20, "sağa")

class ParkurBittiState(VehicleState):
    def handle(self, vehicle, current_yaw, error_yaw):
        try:
            print("Limana yanaşıyor...")
            vehicle.set_velocity_target(5)
            time.sleep(4)
            vehicle.set_velocity_target(5)
            time.sleep(4)

            for _ in range(2):
                local_yaw = vehicle.get_current_yaw()
                rotate_vehicle(vehicle, 45, "sağa")
                time.sleep(4)
        except Exception as e:
            print(f"Liman hatası: {e}")

class BilinmeyenDurumState(VehicleState):
    def handle(self, vehicle, current_yaw, error_yaw):
        try:
            print("Bilinmeyen durum. Duran mod.")
            vehicle.set_velocity_target(0)
            vehicle.set_yaw_target(current_yaw)
        except Exception as e:
            print(f"Bilinmeyen durum hatası: {e}")

class VehicleStateHandler:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.state_map = {
            "GOREV YAPILIYOR": GorevYapiliyorState(),
            "KIRMIZI DUBA": KirmiziDubaState(),
            "YESIL DUBA": YesilDubaState(),
            "SARI DUBA": SariDubaState(),
            "PARKUR BITTI, LIMANA YANASIYOR": ParkurBittiState()
        }
        self.default_state = BilinmeyenDurumState()
        self.current_state = self.default_state

    def set_state(self, state_name):
        self.current_state = self.state_map.get(state_name, self.default_state)

    def handle(self, current_yaw, error_yaw):
        self.current_state.handle(self.vehicle, current_yaw, error_yaw)
