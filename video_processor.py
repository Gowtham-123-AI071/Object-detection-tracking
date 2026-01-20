import cv2
import time
from app.services.detector import ObjectDetector
from app.services.tracker import ObjectTracker
from app.services.line_counter import LineCounter
from app.utils.visualization import draw_dashboard
from app.utils.analytics import save_analytics

PERSON = 0
VEHICLES = {2, 3, 5, 7}

class VideoProcessor:
    def __init__(self):
        self.detector = ObjectDetector()
        self.tracker = ObjectTracker()
        self.line = LineCounter(y_line=240)
        self.people_ids = set()
        self.vehicle_ids = set()

        # 🔴 ADDED: persistent heatmap storage
        self.all_heat_points = []

        self.latest_stats = {
            "people": 0,
            "vehicles": 0,
            "line_crossed": 0,
            "fps": 0
        }

    # =========================
    # DESKTOP MODE
    # =========================
    def process_webcam_desktop(self):
        cap = cv2.VideoCapture(0)
        prev = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame, fps = self._process_frame(frame, prev)
            prev = time.time()

            cv2.imshow("Object Detection & Tracking", frame)
            if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:
                break

        cap.release()
        cv2.destroyAllWindows()

    # =========================
    # FASTAPI STREAM MODE
    # =========================
    def process_webcam_stream(self):
        cap = cv2.VideoCapture(0)
        prev = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame, fps = self._process_frame(frame, prev)
            prev = time.time()

            _, buffer = cv2.imencode(".jpg", frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )

        cap.release()

    # =========================
    # SHARED LOGIC
    # =========================
    def _process_frame(self, frame, prev_time):
        frame = cv2.resize(frame, (640, 480))
        detections = self.detector.detect(frame)
        tracked = self.tracker.track(detections, frame)

        heat_points = []  # 🔥 HEATMAP POINTS (x, y)

        for obj in tracked:
            cls = obj.get("class_id", -1)
            bbox = obj.get("bbox")

            if bbox:
                x1, y1, x2, y2 = bbox
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                if cls == PERSON:
                    self.people_ids.add(obj["id"])
                    heat_points.append({"x": cx, "y": cy})

                    # 🔴 ADDED: accumulate heatmap
                    self.all_heat_points.append({"x": cx, "y": cy})

                elif cls in VEHICLES:
                    self.vehicle_ids.add(obj["id"])

                self.line.check_crossing(obj["id"], bbox)

        fps = 1 / (time.time() - prev_time)

        # 🔴 UPDATED CALL (same function, extra data)
        save_analytics(
            len(self.people_ids),
            len(self.vehicle_ids),
            self.line.count,
            fps,
            self.all_heat_points   # 🔴 ADDED
        )

        frame = draw_dashboard(
            frame,
            tracked,
            len(self.people_ids),
            len(self.vehicle_ids),
            self.line.count,
            fps,
            self.line.y_line
        )

        self.latest_stats = {
            "people": len(self.people_ids),
            "vehicles": len(self.vehicle_ids),
            "line_crossed": self.line.count,
            "fps": int(fps)
        }

        return frame, fps
