class WireFrame():
    def __init__(self, name = str, points = list):
        self.name = name
        self.points = points.copy()
        self.type = len(points)

