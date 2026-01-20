import numpy as np

class ZoneHeatmap:
    def __init__(self, width=640, height=480, grid=20):
        self.grid = grid
        self.map = np.zeros((height//grid, width//grid))

    def update(self, bbox):
        x1, y1, x2, y2 = bbox
        cx, cy = (x1+x2)//2, (y1+y2)//2
        gx, gy = cx//self.grid, cy//self.grid
        self.map[gy, gx] += 1

    def get_normalized(self):
        return self.map / (self.map.max() + 1e-6)
