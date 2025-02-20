"""
Author: Bülent Kıpçak
Email: bulentkipcak04@gmail.com
Date: 2024-08-15
Version: 1.0
Description: This project is designed to control a maritime vehicle using the MAVLink protocol using threading.
"""

from abra_ida import AbraIda
import time
import threading

# connection_string = "tcp:192.168.31.60:5760"
connection_string = "tcp:127.0.0.1:5762"
vehicle = AbraIda(connection_string)

vehicle_mode = None
error_yaw = None
vehicle_state = None
current_yaw = 0

data_lock = threading.Lock()

def wait_for_json_data(func, timeout=10):
    start_time = time.time()
    data = None
    while data is None and (time.time() - start_time < timeout):
        data = func()
        if data is None:
            print(f"{func.__name__} verisi bekleniyor...")
            time.sleep(0.1)
    return data

def rotate_vehicle(vehicle, angle, direction="sağa"):
    try:
        current_yaw = vehicle.get_current_yaw()
        target_yaw = current_yaw + angle
        vehicle.set_yaw_target(target_yaw)
        print(f"Diğer dubalar aranıyor, {direction} dönülüyor...")
    except Exception as e:
        print(f"Dönüş sırasında hata oluştu: {e}")

def data_updater():
    global vehicle_mode, error_yaw, vehicle_state, current_yaw

    while True:
        with data_lock:
            vehicle_mode = vehicle.get_current_vehicle_mode()
            vehicle.update_json_mode(vehicle_mode)

            error_yaw = wait_for_json_data(vehicle.read_error_yaw_from_json)
            vehicle_state = wait_for_json_data(vehicle.read_vehicle_state)
            current_yaw = vehicle.get_current_yaw()

        time.sleep(0.2)  

def vehicle_controller():
    global error_yaw, vehicle_state, current_yaw

    while True:
        with data_lock:
            local_error_yaw = error_yaw
            local_vehicle_state = vehicle_state
            local_current_yaw = current_yaw

        if local_error_yaw is None or local_vehicle_state is None:
            time.sleep(0.1)
            continue

        auto_pilot_error_angle = local_error_yaw / 4  #Kamera-otopilot açı oranı
        target_yaw = local_current_yaw + auto_pilot_error_angle

        print(f"Şu anki açı: {local_current_yaw}, Hedef açı: {target_yaw}, Fark: {local_current_yaw - target_yaw}")

        if local_vehicle_state == "GOREV YAPILIYOR":
            try:
                if abs(local_error_yaw) <= 5:
                    print("Yaw açısı hedef farkı ±5 dereceden küçük, 4m/s ileri hız ayarlanıyor.")
                    vehicle.set_velocity_target(4)
                else:
                    print("Yaw açısı hedef farkı ±5 dereceden büyük, sadece hedef açı ayarlanıyor.")
                    vehicle.set_yaw_target(target_yaw)
            except Exception as e:
                print(f"Görev sırasında hata oluştu: {e}")

        elif local_vehicle_state == "KIRMIZI DUBA":
            rotate_vehicle(vehicle, 10, "sağa")

        elif local_vehicle_state == "YESIL DUBA":
            rotate_vehicle(vehicle, -10, "sola")

        elif local_vehicle_state == "SARI DUBA":
            rotate_vehicle(vehicle, -10, "sola")
            time.sleep(5)
            rotate_vehicle(vehicle, 20, "sağa")

        elif local_vehicle_state == "PARKUR BITTI, LIMANA YANASIYOR":
            try:
                print("Limana yanaşıyor...")
                vehicle.set_velocity_target(5)
                time.sleep(4)
                vehicle.set_velocity_target(5)
                time.sleep(4)

                for _ in range(2):
                    local_current_yaw = vehicle.get_current_yaw()
                    rotate_vehicle(vehicle, 45, "sağa")
                    time.sleep(4)

            except Exception as e:
                print(f"Liman yanaşma sırasında hata oluştu: {e}")

        else:
            try:
                vehicle.set_velocity_target(0)
                vehicle.set_yaw_target(vehicle.get_current_yaw())
                print("Bilinmeyen durum.")
            except Exception as e:
                print(f"Bilinmeyen durumda hata oluştu: {e}")

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
