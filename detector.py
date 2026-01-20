from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="models/yolov8n.pt"):
        self.model = YOLO("yolov8n.pt")


    def detect(self, frame):
        results = self.model(frame, stream=True)
        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence,
                    "class_id": class_id
                })

        return detections
