class MultiLineCounter:
    def __init__(self, lines):
        """
        lines = {
          "entry": 200,
          "exit": 350
        }
        """
        self.lines = lines
        self.crossed = {k: set() for k in lines}
        self.counts = {k: 0 for k in lines}

    def update(self, obj_id, bbox):
        _, y1, _, y2 = bbox
        cy = (y1 + y2) // 2

        for name, y_line in self.lines.items():
            if obj_id not in self.crossed[name] and cy > y_line:
                self.crossed[name].add(obj_id)
                self.counts[name] += 1

        return self.counts
