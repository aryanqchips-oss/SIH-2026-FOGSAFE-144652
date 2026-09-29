from ultralytics import YOLO


class FogSafeDetector:

    def __init__(self):

        self.model = YOLO("yolo11s.pt")

    def detect(self, frame):

        results = self.model(
            frame,
            verbose=False
        )

        detections = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = self.model.names[class_id]

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                detections.append({
                    "object": class_name.upper(),
                    "confidence": round(confidence * 100, 1),
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                })

        return detections