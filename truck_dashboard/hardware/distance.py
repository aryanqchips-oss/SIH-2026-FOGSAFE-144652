import time

import RPi.GPIO as GPIO

from hardware.config import (
    HC_SR04_TRIGGER_PIN,
    HC_SR04_ECHO_PIN,
    SIMULATION_MODE
)


class DistanceSensor:

    def __init__(self):

        self.distance = 0.0
        self.status = "NORMAL"

        if not SIMULATION_MODE:
            self.setup_hardware()

    def setup_hardware(self):

        try:

            GPIO.setmode(GPIO.BCM)

            GPIO.setup(
                HC_SR04_TRIGGER_PIN,
                GPIO.OUT
            )

            GPIO.setup(
                HC_SR04_ECHO_PIN,
                GPIO.IN
            )

            GPIO.output(
                HC_SR04_TRIGGER_PIN,
                GPIO.LOW
            )

            time.sleep(0.5)

            self.status = "NORMAL"

        except Exception as e:

            print(
                "HC-SR04 initialization error:",
                e
            )

            self.status = "ERROR"

    def read(self):

        if SIMULATION_MODE:

            return {
                "distance": 6.0,
                "status": "NORMAL"
            }

        return self.read_hardware()

    def read_hardware(self):

        try:

            GPIO.output(
                HC_SR04_TRIGGER_PIN,
                GPIO.LOW
            )

            time.sleep(0.000002)

            GPIO.output(
                HC_SR04_TRIGGER_PIN,
                GPIO.HIGH
            )

            time.sleep(0.00001)

            GPIO.output(
                HC_SR04_TRIGGER_PIN,
                GPIO.LOW
            )

            timeout = time.time() + 0.03

            while GPIO.input(
                HC_SR04_ECHO_PIN
            ) == 0:

                pulse_start = time.time()

                if pulse_start > timeout:
                    raise TimeoutError(
                        "Echo start timeout"
                    )

            timeout = time.time() + 0.03

            while GPIO.input(
                HC_SR04_ECHO_PIN
            ) == 1:

                pulse_end = time.time()

                if pulse_end > timeout:
                    raise TimeoutError(
                        "Echo end timeout"
                    )

            pulse_duration = (
                pulse_end -
                pulse_start
            )

            distance = (
                pulse_duration *
                34300
            ) / 2

            if distance < 2 or distance > 400:

                self.status = "OUT OF RANGE"

                return {
                    "distance": 0.0,
                    "status": self.status
                }

            self.distance = round(
                distance / 100,
                2
            )

            self.status = "NORMAL"

            return {
                "distance": self.distance,
                "status": self.status
            }

        except Exception as e:

            print(
                "HC-SR04 read error:",
                e
            )

            self.status = "ERROR"

            return {
                "distance": 0.0,
                "status": self.status
            }