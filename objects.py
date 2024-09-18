import numpy
import math

class Point():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_x(self) -> float:
        return self.x
    
    def get_y(self) -> float:
        return self.y
    
    def set_x(self, x) -> None:
        self.x = x
        
    def set_y(self, y) -> None:
        self.y = y
    
    def get_str_point(self) -> str:
        return "("+str(self.get_x())+","+str(self.get_y())+")"

        
class WireFrame():
    def __init__(self, name: str, points: list[Point]):
        self.name = name
        self.type = str(len(points))
        self.points = points
        self.transform_matrix = numpy.identity(3)
        self.center = self.set_center()
        #self.transform_matrix = self.transform_matrix.dot(numpy.array([[0,0,0],[0,0,0],[10,10,1]]))
        print(self.get_center().get_str_point())

    def get_name(self) -> str:
        return self.name
    
    def get_type(self) -> int:
        return self.type

    def get_points(self) -> list:
        return self.points
    
    def get_str_points(self) -> str:
        str_point = ""
        
        for p in self.points:
            str_point += "("+str(p.get_x())+","+str(p.get_y())+")"
            
        return str_point
    
    def set_center(self) -> Point:
        xsum = 0
        ysum = 0
        for point in self.points:
            xsum = xsum + point.get_x()
            ysum = ysum + point.get_y()
        x = xsum/len(self.points)
        y = ysum/len(self.points)
        return Point(x, y)
    
    def get_center(self) -> Point:
        return self.center
    
    def get_transform(self):
        return self.transform_matrix
    
    def reset_transform(self):
        self.transform_matrix = numpy.identity(3)
    
    def apply_transform(self): #lembrete de rodar reset_transform() depois
        print(self.get_transform())
        for point in self.points:
            point_matrix = numpy.array([point.get_x(), point.get_y(), 1])
            point_matrix = point_matrix.dot(self.transform_matrix)
            point.set_x(point_matrix[0])
            point.set_y(point_matrix[1])
        self.set_center()
    
    def transform_scaling(self,sx,sy):
        pivot = self.get_center()
        self.transform_translate(-pivot.get_x(), -pivot.get_y())
        self.transform_basic_scaling(sx,sy)
        self.transform_translate(self.center.get_x(), self.center.get_y())
    
    def transform_rotation(self,angle, pivot: Point):
        #pivot = self.get_center()
        self.transform_translate(-pivot.get_x(), -pivot.get_y())
        self.transform_basic_rotation(angle)
        self.transform_translate(pivot.get_x(), pivot.get_y())
        

    def transform_translate(self, dx, dy):
        translation = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        self.transform_matrix = self.transform_matrix.dot(translation)
        self.set_center()
    
    def transform_basic_scaling(self, sx, sy):
        scaling = numpy.array([[sx, 0, 0],[0, sy, 0],[0, 0, 1]])
        self.transform_matrix = self.transform_matrix.dot(scaling)
        self.set_center()
    
    def transform_basic_rotation(self, angle):
        angle_rad = math.radians(angle)
        rotation = numpy.array([[math.cos(angle_rad), -math.sin(angle_rad), 0],[math.sin(angle_rad),math.cos(angle_rad),0],[0, 0, 1]])
        self.transform_matrix = self.transform_matrix.dot(rotation)
        self.set_center()
        #print(self.transform_matrix)
    
