import serial
import pynmea2

from hardware.config import (
    GPS_PORT,
    GPS_BAUDRATE,
    SIMULATION_MODE
)


class GPS:

    def __init__(self):

        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.speed = 0.0
        self.heading = 0.0
        self.status = "NO FIX"

        self.serial = None

        if not SIMULATION_MODE:
            self.setup_hardware()

    def setup_hardware(self):

        try:
            self.serial = serial.Serial(
                GPS_PORT,
                GPS_BAUDRATE,
                timeout=1
            )

            self.status = "SEARCHING"

        except Exception as e:

            print("GPS initialization error:", e)
            self.serial = None
            self.status = "ERROR"

    def read(self):

        if SIMULATION_MODE:

            return {
                "latitude": 19.0760,
                "longitude": 72.8777,
                "altitude": 45.0,
                "speed": 8.4,
                "heading": 135.0,
                "status": "FIXED"
            }

        return self.read_hardware()

    def read_hardware(self):

        if self.serial is None:

            return {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "altitude": self.altitude,
                "speed": self.speed,
                "heading": self.heading,
                "status": "ERROR"
            }

        try:

            for _ in range(10):

                line = self.serial.readline().decode(
                    "ascii",
                    errors="ignore"
                ).strip()

                if not line:
                    continue

                try:

                    message = pynmea2.parse(line)

                except pynmea2.ParseError:
                    continue

                if isinstance(message, pynmea2.types.talker.GGA):

                    if message.latitude and message.longitude:

                        self.latitude = message.latitude
                        self.longitude = message.longitude

                    if message.altitude:
                        self.altitude = float(
                            message.altitude
                        )

                    if message.gps_qual:
                        self.status = "FIXED"

                elif isinstance(
                    message,
                    pynmea2.types.talker.RMC
                ):

                    if message.latitude and message.longitude:

                        self.latitude = message.latitude
                        self.longitude = message.longitude

                    if message.spd_over_grnd:
                        self.speed = float(
                            message.spd_over_grnd
                        ) * 1.852

                    if message.true_course:
                        self.heading = float(
                            message.true_course
                        )

                    if message.status == "A":
                        self.status = "FIXED"
                    else:
                        self.status = "NO FIX"

            return {
                "latitude": round(
                    self.latitude,
                    6
                ),
                "longitude": round(
                    self.longitude,
                    6
                ),
                "altitude": round(
                    self.altitude,
                    1
                ),
                "speed": round(
                    self.speed,
                    1
                ),
                "heading": round(
                    self.heading,
                    1
                ),
                "status": self.status
            }

        except Exception as e:

            print("GPS read error:", e)

            self.status = "ERROR"

            return {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "altitude": self.altitude,
                "speed": self.speed,
                "heading": self.heading,
                "status": self.status
            }