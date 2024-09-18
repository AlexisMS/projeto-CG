import numpy
import math

class Point():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y
    
    def set_x(self, x) -> None:
        self.x = x
        
    def set_y(self, y) -> None:
        self.y = y
        
class WireFrame():
    def __init__(self, name: str, points: list[Point]):
        self.name = name
        self.type = str(len(points))
        self.points = points
        self.transform_matrix = numpy.identity(3)
        self.center = self.get_center()
        #self.transform_matrix = self.transform_matrix.dot(numpy.array([[0,0,0],[0,0,0],[10,10,1]]))
        print(self.transform_matrix)

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
    
    def get_center(self) -> Point:
        xsum = 0
        ysum = 0
        for point in self.points:
            xsum = xsum + point.get_x()
            ysum = ysum + point.get_y()
        x = xsum/len(self.points)
        y = ysum/len(self.points)
        return Point(x, y)
    
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
    
    def transform_scaling(self,sx,sy):
        distance_to_origin = math.sqrt(pow(-self.center.get_x(),2)+pow(-self.center.get_y(),2))
        if self.center.get_x()>0 and self.center.get_y()>0:
            self.transform_translate(self, -distance_to_origin, -distance_to_origin)
            self.transform_basic_scaling(self,sx,sy)
            self.transform_translate(self, distance_to_origin, distance_to_origin)
        elif self.center.get_x()>0 and self.center.get_y()<0:
            self.transform_translate(self, -distance_to_origin, distance_to_origin)
            self.transform_basic_scaling(self,sx,sy)
            self.transform_translate(self, distance_to_origin, -distance_to_origin)
        elif self.center.get_x()<0 and self.center.get_y()<0:
            self.transform_translate(self, distance_to_origin, distance_to_origin)
            self.transform_basic_scaling(self,sx,sy)
            self.transform_translate(self, -distance_to_origin, -distance_to_origin)
        elif self.center.get_x()==0 and self.center.get_y()>0:
            self.transform_translate(self, 0, -distance_to_origin)
            self.transform_basic_scaling(self,sx,sy)
            self.transform_translate(self, 0, distance_to_origin)
        elif self.center.get_x()==0 and self.center.get_y()<0:
            self.transform_translate(self, 0, distance_to_origin)
            self.transform_basic_scaling(self,sx,sy)
            self.transform_translate(self, 0, -distance_to_origin)
        elif self.center.get_x()>0 and self.center.get_y()==0:
            self.transform_translate(self, -distance_to_origin, 0)
            self.transform_basic_scaling(self,sx,sy)
            self.transform_translate(self, distance_to_origin, 0)
        elif self.center.get_x()<0 and self.center.get_y()==0:
            self.transform_translate(self, distance_to_origin, 0)
            self.transform_basic_scaling(self,sx,sy)
            self.transform_translate(self, -distance_to_origin, 0)
        elif self.center.get_x()==0 and self.center.get_y()==0:
            self.transform_basic_scaling(self,sx,sy)
    
    def transform_rotation(self, angle):
        distance_to_origin = math.sqrt(pow(-self.center.get_x(),2)+pow(-self.center.get_y(),2))
        if self.center.get_x()>0 and self.center.get_y()>0:
            self.transform_translate(self, -distance_to_origin, -distance_to_origin)
            self.transform_basic_rotation(self,angle)
            self.transform_translate(self, distance_to_origin, distance_to_origin)
        elif self.center.get_x()>0 and self.center.get_y()<0:
            self.transform_translate(self, -distance_to_origin, distance_to_origin)
            self.transform_basic_rotation(self,angle)
            self.transform_translate(self, distance_to_origin, -distance_to_origin)
        elif self.center.get_x()<0 and self.center.get_y()<0:
            self.transform_translate(self, distance_to_origin, distance_to_origin)
            self.transform_basic_rotation(self,angle)
            self.transform_translate(self, -distance_to_origin, -distance_to_origin)
        elif self.center.get_x()==0 and self.center.get_y()>0:
            self.transform_translate(self, 0, -distance_to_origin)
            self.transform_basic_rotation(self,angle)
            self.transform_translate(self, 0, distance_to_origin)
        elif self.center.get_x()==0 and self.center.get_y()<0:
            self.transform_translate(self, 0, distance_to_origin)
            self.transform_basic_rotation(self,angle)
            self.transform_translate(self, 0, -distance_to_origin)
        elif self.center.get_x()>0 and self.center.get_y()==0:
            self.transform_translate(self, -distance_to_origin, 0)
            self.transform_basic_rotation(self,angle)
            self.transform_translate(self, distance_to_origin, 0)
        elif self.center.get_x()<0 and self.center.get_y()==0:
            self.transform_translate(self, distance_to_origin, 0)
            self.transform_basic_rotation(self,angle)
            self.transform_translate(self, -distance_to_origin, 0)
        elif self.center.get_x()==0 and self.center.get_y()==0:
            self.transform_basic_rotation(self,angle)
        

    def transform_translate(self, dx, dy):
        translation = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        self.transform_matrix = self.transform_matrix.dot(translation)
    
    def transform_basic_scaling(self, sx, sy):
        scaling = numpy.array([[sx, 0, 0],[0, sy, 0],[0, 0, 1]])
        self.transform_matrix = self.transform_matrix.dot(scaling)
    
    def transform_basic_rotation(self, angle):
        angle_rad = math.radians(angle)
        rotation = numpy.array([[math.cos(angle_rad), -math.sin(angle_rad), 0],[math.sin(angle_rad),math.cos(angle_rad),0],[0, 0, 1]])
        self.transform_matrix = self.transform_matrix.dot(rotation)
        print(self.transform_matrix)
    
