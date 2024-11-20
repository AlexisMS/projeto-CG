from display_file import DisplayFile
from objects import Point
from transform_functions import *
import numpy


class Window():
    def __init__(self, xmin:int, ymin:int, zmin:int,
                 xmax:int,ymax:int, zmax:int,
                 u:int, v: int,
                 display_file: DisplayFile):
        self.xmin = xmin
        self.ymin = ymin
        self.zmin = zmin
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        self.u = u
        self.v = v
        self.n = 0
        # self.vpn
        self.shift = Point3D(0,0,0)
        self.center = Point3D((xmax + xmin)/2, (ymax + ymin)/2, (zmax + zmin)/2)
        self.display_file = display_file
        self.normalization_matrix = numpy.identity(3)
        self.ortogonal_projection_matrix = numpy.identity(4)
        self.angle = 0
        self.zoom = 0
        self.update_normalization_matrix()
        self.update_ortogonal_projection_matrix()

    def update_ortogonal_projection_matrix(self):
        dx = self.shift.get_x()
        dy = self.shift.get_y()
        dz = self.shift.get_z()
        self.ortogonal_projection_matrix = build_ortogonal_projection_matrix(dx, dy, dz, self.u, self.v)

    def update_normalization_matrix(self) -> None:
        height = self.ymax - self.ymin
        widht = self.xmax - self.xmin
        self.normalization_matrix = build_normalization_matrix(height, widht, self.shift, self.angle)

    def update_center(self) -> None:
        self.center = Point3D((self.xmax + self.xmin)/2, (self.ymax + self.ymin)/2, (self.zmax + self.zmin)/2)

    def get_ortogonal_projection_matrix(self) -> numpy.ndarray:
        return self.ortogonal_projection_matrix

    def get_normalization_matrix(self) -> numpy.ndarray:
        return self.normalization_matrix
    
    def get_display_file(self) -> DisplayFile:
        return self.display_file

    def get_shift(self) -> Point:
        return self.shift

    def get_center(self) -> Point3D:
        return self.center
    
    def get_u(self):
        return self.u
    
    def get_v(self):
        return self.v
    
    def get_xmax(self) -> float:
        return self.xmax
    
    def get_ymax(self) -> float:
        return self.ymax
    
    def get_zmax(self) -> float:
        return self.zmax
    
    def get_xmin(self) -> float:
        return self.xmin
    
    def get_ymin(self) -> float:
        return self.ymin
    
    def get_zmin(self) -> float:
        return self.zmin
    
    def set_angle(self, angle) -> None:
        self.angle -= angle

    def set_u(self, u):
        self.u = u

    def set_v(self, v):
        self.v = v
    
    def set_xmax(self, xmax:int) -> None:
        self.xmax = xmax

    def set_ymax(self, ymax:int) -> None:
        self.ymax = ymax

    def set_zmax(self, zmax:int) -> None:
        self.zmax = zmax

    def set_xmin(self, xmin:int) -> None:
        self.xmin = xmin
    
    def set_ymin(self, ymin:int) -> None:
        self.ymin = ymin

    def set_zmin(self, zmin:int) -> None:
        self.zmin = zmin
