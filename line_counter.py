class LineCounter:
    def __init__(self, y_line=240):
        self.y_line = y_line
        self.crossed_ids = set()
        self.count = 0

    def check_crossing(self, obj_id, bbox):
        _, y1, _, y2 = bbox
        center_y = (y1 + y2) // 2

        if obj_id not in self.crossed_ids and center_y > self.y_line:
            self.crossed_ids.add(obj_id)
            self.count += 1

        return self.count
