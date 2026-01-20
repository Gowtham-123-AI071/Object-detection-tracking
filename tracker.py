from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectTracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)

    def track(self, detections, frame):
        inputs = []

        for d in detections:
            x1, y1, x2, y2 = d["bbox"]
            w, h = x2 - x1, y2 - y1
            inputs.append(([x1, y1, w, h], d["confidence"], d["class_id"]))

        tracks = self.tracker.update_tracks(inputs, frame=frame)
        objects = []

        for t in tracks:
            if not t.is_confirmed():
                continue

            l, t_, r, b = map(int, t.to_ltrb())

            objects.append({
                "id": t.track_id,
                "bbox": [l, t_, r, b],
                # ✅ SAFE: det_class may be None
                "class_id": t.det_class if t.det_class is not None else -1
            })

        return objects
