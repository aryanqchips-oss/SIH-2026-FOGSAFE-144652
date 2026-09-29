import math
import time

from smbus2 import SMBus

from hardware.config import (
    MPU6050_ADDRESS,
    SIMULATION_MODE
)


class IMU:

    def __init__(self):

        self.acceleration = 0.0
        self.tilt = 0.0
        self.speed = 0.0
        self.heading = 0.0
        self.status = "NORMAL"

        self.bus = None

        if not SIMULATION_MODE:
            self.setup_hardware()

    def setup_hardware(self):

        try:

            self.bus = SMBus(1)

            self.bus.write_byte_data(
                MPU6050_ADDRESS,
                0x6B,
                0
            )

            time.sleep(0.1)

            self.status = "NORMAL"

        except Exception as e:

            print("MPU6050 initialization error:", e)

            self.bus = None
            self.status = "ERROR"

    def read_raw(self, register):

        high = self.bus.read_byte_data(
            MPU6050_ADDRESS,
            register
        )

        low = self.bus.read_byte_data(
            MPU6050_ADDRESS,
            register + 1
        )

        value = (high << 8) | low

        if value >= 32768:
            value -= 65536

        return value

    def read(self):

        if SIMULATION_MODE:

            return {
                "speed": 0.0,
                "heading": 0.0,
                "acceleration": 0.8,
                "tilt": 2.1,
                "status": "NORMAL"
            }

        return self.read_hardware()

    def read_hardware(self):

        if self.bus is None:

            return {
                "speed": 0.0,
                "heading": 0.0,
                "acceleration": 0.0,
                "tilt": 0.0,
                "status": "ERROR"
            }

        try:

            ax_raw = self.read_raw(0x3B)
            ay_raw = self.read_raw(0x3D)
            az_raw = self.read_raw(0x3F)

            ax = ax_raw / 16384.0
            ay = ay_raw / 16384.0
            az = az_raw / 16384.0

            total_acceleration = math.sqrt(
                ax * ax +
                ay * ay +
                az * az
            )

            acceleration = abs(
                total_acceleration - 1.0
            ) * 9.81

            tilt = math.degrees(
                math.atan2(
                    ax,
                    math.sqrt(
                        ay * ay +
                        az * az
                    )
                )
            )

            self.acceleration = round(
                acceleration,
                2
            )

            self.tilt = round(
                tilt,
                1
            )

            self.status = "NORMAL"

            return {
                "speed": self.speed,
                "heading": self.heading,
                "acceleration": self.acceleration,
                "tilt": self.tilt,
                "status": self.status
            }

        except Exception as e:

            print("MPU6050 read error:", e)

            self.status = "ERROR"

            return {
                "speed": self.speed,
                "heading": self.heading,
                "acceleration": self.acceleration,
                "tilt": self.tilt,
                "status": self.status
            }