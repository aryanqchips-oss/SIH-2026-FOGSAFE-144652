from hardware.gps import GPS
from hardware.imu import IMU
from hardware.distance import DistanceSensor


class SensorManager:

    def __init__(self):

        self.gps = GPS()
        self.imu = IMU()
        self.distance = DistanceSensor()

    def read_all(self):

        gps_data = self.gps.read()
        imu_data = self.imu.read()
        distance_data = self.distance.read()

        imu_data["speed"] = gps_data.get(
            "speed",
            imu_data.get("speed", 0.0)
        )

        imu_data["heading"] = gps_data.get(
            "heading",
            imu_data.get("heading", 0.0)
        )

        return {
            "gps": gps_data,
            "imu": imu_data,
            "distance": distance_data
        }