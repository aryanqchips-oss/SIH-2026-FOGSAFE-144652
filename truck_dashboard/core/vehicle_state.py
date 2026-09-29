import random


class VehicleState:

    def __init__(self):

        self.speed = 8.4
        self.recommended_speed = 10.0

        self.object = "NONE"
        self.confidence = 0.0
        self.distance = 0.0
        self.direction = "CLEAR"
        self.safety = "CONTINUE"

        self.visibility = 8.0
        self.fog_level = "CLEAR"

        self.latitude = 19.0760
        self.longitude = 72.8777
        self.altitude = 45.0

        self.heading = 135.0
        self.acceleration = 0.8
        self.tilt = 2.1

        self.gps_status = "FIXED"
        self.imu_status = "NORMAL"
        self.distance_sensor_status = "NORMAL"

        self.system_status = "NORMAL"


    # =========================================
    # SENSOR DATA
    # =========================================

    def update_sensors(self, sensor_data):

        gps = sensor_data.get("gps", {})
        imu = sensor_data.get("imu", {})
        distance = sensor_data.get("distance", {})


        # GPS

        self.latitude = gps.get(
            "latitude",
            self.latitude
        )

        self.longitude = gps.get(
            "longitude",
            self.longitude
        )

        self.altitude = gps.get(
            "altitude",
            self.altitude
        )

        self.gps_status = gps.get(
            "status",
            self.gps_status
        )


        # IMU

        self.speed = imu.get(
            "speed",
            self.speed
        )

        self.heading = imu.get(
            "heading",
            self.heading
        )

        self.acceleration = imu.get(
            "acceleration",
            self.acceleration
        )

        self.tilt = imu.get(
            "tilt",
            self.tilt
        )

        self.imu_status = imu.get(
            "status",
            self.imu_status
        )


        # Distance sensor

        self.distance_sensor_status = distance.get(
            "status",
            self.distance_sensor_status
        )


    # =========================================
    # OBJECT DETECTION
    # =========================================

    def update_object(
        self,
        object_name,
        confidence,
        distance,
        direction
    ):

        self.object = object_name

        self.confidence = confidence

        self.distance = distance

        self.direction = direction


    # =========================================
    # SAFETY
    # =========================================

    def update_safety(
        self,
        safety,
        recommended_speed
    ):

        self.safety = safety

        self.recommended_speed = recommended_speed


    # =========================================
    # VISIBILITY
    # =========================================

    def update_visibility(self):

        self.visibility += random.uniform(
            -0.25,
            0.25
        )

        self.visibility = max(
            2.0,
            min(10.0, self.visibility)
        )


        if self.visibility >= 8:

            self.fog_level = "CLEAR"

        elif self.visibility >= 6:

            self.fog_level = "MODERATE FOG"

        elif self.visibility >= 4:

            self.fog_level = "DENSE FOG"

        else:

            self.fog_level = "VERY DENSE FOG"


        if self.visibility >= 8:

            self.recommended_speed = 15.0

        elif self.visibility >= 6:

            self.recommended_speed = 10.0

        elif self.visibility >= 4:

            self.recommended_speed = 7.0

        else:

            self.recommended_speed = 4.0


    # =========================================
    # GET DATA
    # =========================================

    def get_data(self):

        self.update_visibility()

        return {

            "speed":
                round(self.speed, 1),

            "recommended_speed":
                round(
                    self.recommended_speed,
                    1
                ),

            "object":
                self.object,

            "confidence":
                round(
                    self.confidence,
                    1
                ),

            "distance":
                round(
                    self.distance,
                    1
                ),

            "direction":
                self.direction,

            "safety":
                self.safety,

            "visibility":
                round(
                    self.visibility,
                    1
                ),

            "fog_level":
                self.fog_level,

            "latitude":
                self.latitude,

            "longitude":
                self.longitude,

            "altitude":
                self.altitude,

            "heading":
                self.heading,

            "acceleration":
                self.acceleration,

            "tilt":
                self.tilt,

            "gps_status":
                self.gps_status,

            "imu_status":
                self.imu_status,

            "distance_sensor_status":
                self.distance_sensor_status,

            "system_status":
                self.system_status
        }