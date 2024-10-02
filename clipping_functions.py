from objects import WireFrame

def liang_barsky(obj: WireFrame):
    points = obj.get_points()
    point1 = points[0]
    point2 = points[1]
    p1 = -(point2.get_x() - point1.get_x())
    p1 = -(point2.get_x() - point1.get_x())