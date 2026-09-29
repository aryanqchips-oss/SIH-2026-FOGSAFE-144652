from flask import Flask, Response, jsonify, request, render_template
import cv2
import base64
import numpy as np

from ai.detector import FogSafeDetector
from core.vehicle_state import VehicleState
from hardware.sensor_manager import SensorManager


app = Flask(__name__)


# ============================================================
# INITIALIZE SYSTEM
# ============================================================

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

detector = FogSafeDetector()

vehicle = VehicleState()

sensors = SensorManager()

latest_detections = []


# ============================================================
# CAMERA DISTANCE ESTIMATION
# Prototype estimate only
# ============================================================

def estimate_distance(detection, frame_height):

    y1 = detection["y1"]
    y2 = detection["y2"]

    object_height = y2 - y1

    if object_height <= 0:
        return 10.0

    relative_height = object_height / frame_height

    if relative_height >= 0.65:
        distance = 1.5

    elif relative_height >= 0.50:
        distance = 2.5

    elif relative_height >= 0.40:
        distance = 3.5

    elif relative_height >= 0.30:
        distance = 4.5

    elif relative_height >= 0.22:
        distance = 6.0

    elif relative_height >= 0.15:
        distance = 8.0

    else:
        distance = 10.0

    return distance


# ============================================================
# OBJECT DIRECTION
# ============================================================

def calculate_direction(detection, frame_width):

    center_x = (
        detection["x1"] +
        detection["x2"]
    ) / 2

    if center_x < frame_width * 0.33:
        return "LEFT"

    elif center_x > frame_width * 0.66:
        return "RIGHT"

    else:
        return "AHEAD"


# ============================================================
# SENSOR UPDATE
# ============================================================

def update_sensor_state():

    sensor_data = sensors.read_all()

    vehicle.update_sensors(sensor_data)

    return sensor_data


# ============================================================
# SENSOR FUSION
# ============================================================

def fuse_sensor_data(
    object_distance,
    sensor_distance,
    visibility,
    vehicle_speed
):

    if sensor_distance is not None and sensor_distance > 0:

        final_distance = min(
            object_distance,
            sensor_distance
        )

    else:

        final_distance = object_distance

    # --------------------------------------------------------
    # Safety decision
    # --------------------------------------------------------

    if final_distance <= 3.5:

        safety = "STOP"

    elif final_distance <= 8.0:

        safety = "CAUTION"

    else:

        safety = "CONTINUE"

    # --------------------------------------------------------
    # Fog adjustment
    # --------------------------------------------------------

    if visibility < 4.0:

        if final_distance <= 5.0:

            safety = "STOP"

        elif final_distance <= 10.0:

            safety = "CAUTION"

    # --------------------------------------------------------
    # Recommended speed
    # --------------------------------------------------------

    if safety == "STOP":

        recommended_speed = 0.0

    elif safety == "CAUTION":

        if visibility < 4.0:

            recommended_speed = 4.0

        elif visibility < 6.0:

            recommended_speed = 7.0

        else:

            recommended_speed = 10.0

    else:

        if visibility >= 8.0:

            recommended_speed = 15.0

        elif visibility >= 6.0:

            recommended_speed = 10.0

        elif visibility >= 4.0:

            recommended_speed = 7.0

        else:

            recommended_speed = 4.0

    # --------------------------------------------------------
    # Vehicle speed safety check
    # --------------------------------------------------------

    if (
        vehicle_speed > recommended_speed
        and safety == "CONTINUE"
    ):

        safety = "CAUTION"

    return (
        final_distance,
        safety,
        recommended_speed
    )


# ============================================================
# CAMERA STREAM
# ============================================================

def generate_frames():

    global latest_detections

    while True:

        success, frame = camera.read()

        if not success:

            continue

        # ----------------------------------------------------
        # Update sensor data
        # ----------------------------------------------------

        sensor_data = update_sensor_state()

        imu_data = sensor_data.get(
            "imu",
            {}
        )

        distance_data = sensor_data.get(
            "distance",
            {}
        )

        sensor_distance = distance_data.get(
            "distance",
            None
        )

        vehicle_speed = imu_data.get(
            "speed",
            0
        )

        # ----------------------------------------------------
        # YOLO detection
        # ----------------------------------------------------

        detections = detector.detect(frame)

        latest_detections = detections

        # ----------------------------------------------------
        # No object detected
        # ----------------------------------------------------

        if not detections:

            vehicle.update_object(
                "NONE",
                0.0,
                0.0,
                "CLEAR"
            )

            vehicle.update_safety(
                "CONTINUE",
                vehicle.recommended_speed
            )

        # ----------------------------------------------------
        # Object detected
        # ----------------------------------------------------

        else:

            best_detection = max(
                detections,
                key=lambda x: x["confidence"]
            )

            object_name = best_detection.get(
                "class_name",
                best_detection.get(
                    "class",
                    "OBJECT"
                )
            )

            confidence = best_detection.get(
                "confidence",
                0
            )

            # Camera distance estimate

            camera_distance = estimate_distance(
                best_detection,
                frame.shape[0]
            )

            # Object direction

            direction = calculate_direction(
                best_detection,
                frame.shape[1]
            )

            # ------------------------------------------------
            # Sensor fusion
            # ------------------------------------------------

            (
                final_distance,
                safety,
                recommended_speed
            ) = fuse_sensor_data(
                camera_distance,
                sensor_distance,
                vehicle.visibility,
                vehicle_speed
            )

            # Update vehicle state

            vehicle.update_object(
                object_name,
                confidence,
                final_distance,
                direction
            )

            vehicle.update_safety(
                safety,
                recommended_speed
            )

            # ------------------------------------------------
            # Draw detection
            # ------------------------------------------------

            x1 = int(best_detection["x1"])
            y1 = int(best_detection["y1"])
            x2 = int(best_detection["x2"])
            y2 = int(best_detection["y2"])

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = (
                f"{object_name} "
                f"{confidence:.0f}% "
                f"{final_distance:.1f}m"
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # ----------------------------------------------------
        # Encode frame
        # ----------------------------------------------------

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not ret:

            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ============================================================
# LIVE VIDEO
# ============================================================

@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ============================================================
# DETECTIONS API
# ============================================================

@app.route("/api/detections")
def get_detections():

    return jsonify({
        "success": True,
        "detections": latest_detections
    })


# ============================================================
# VEHICLE API
# ============================================================

@app.route("/api/vehicle")
def get_vehicle():

    update_sensor_state()

    return jsonify(
        vehicle.get_data()
    )


# ============================================================
# IMAGE ANALYSIS
# ============================================================

@app.route(
    "/api/analyze-image",
    methods=["POST"]
)
def analyze_image():

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "error": "No image uploaded"
        }), 400

    file = request.files["image"]

    if file.filename == "":

        return jsonify({
            "success": False,
            "error": "No image selected"
        }), 400

    file_bytes = file.read()

    image_array = np.frombuffer(
        file_bytes,
        np.uint8
    )

    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if frame is None:

        return jsonify({
            "success": False,
            "error": "Invalid image"
        }), 400

    # --------------------------------------------------------
    # YOLO detection
    # --------------------------------------------------------

    detections = detector.detect(
        frame
    )

    # --------------------------------------------------------
    # Draw detections
    # --------------------------------------------------------

    for detection in detections:

        x1 = int(detection["x1"])
        y1 = int(detection["y1"])
        x2 = int(detection["x2"])
        y2 = int(detection["y2"])

        class_name = detection.get(
            "class_name",
            detection.get(
                "class",
                "OBJECT"
            )
        )

        confidence = detection.get(
            "confidence",
            0
        )

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        label = (
            f"{class_name} "
            f"{confidence:.0f}%"
        )

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # --------------------------------------------------------
    # Encode result
    # --------------------------------------------------------

    success, buffer = cv2.imencode(
        ".jpg",
        frame
    )

    if not success:

        return jsonify({
            "success": False,
            "error": "Could not encode image"
        }), 500

    encoded_image = base64.b64encode(
        buffer
    ).decode("utf-8")

    return jsonify({

        "success": True,

        "image": (
            "data:image/jpeg;base64,"
            + encoded_image
        ),

        "detections": detections,

        "count": len(detections)

    })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )