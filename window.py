from display_file import DisplayFile
from objects import Point
from transform_functions import *
import numpy


class Window():
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int, display_file: DisplayFile):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.xmin_normalized = None
        self.ymin_normalized = None
        self.xmax_normalized = None
        self.ymax_normalized = None
        self.shift = Point(0,0)
        self.center = Point((xmax + xmin)/2, (ymax + ymin)/2)
        self.display_file = display_file
        self.normalization_matrix = numpy.identity(3)
        self.angle = 0
        self.zoom = 0
        self.update_normalization_matrix()

    def get_normalization_matrix(self) -> numpy.ndarray:
        return self.normalization_matrix
    
    def update_normalized_coord(self) -> None:
        coord_min = numpy.array([self.xmin, self.ymin, 1])
        coord_min = coord_min.dot(self.normalization_matrix)
        coord_max = numpy.array([self.xmax, self.ymax, 1])
        coord_max = coord_max.dot(self.normalization_matrix)
        self.xmin_normalized = coord_min[0]
        self.ymin_normalized = coord_min[1]
        self.xmax_normalized = coord_max[0]
        self.ymax_normalized = coord_max[1]

    def update_normalization_matrix(self) -> None:
        height = self.ymax - self.ymin
        widht = self.xmax - self.xmin
        self.normalization_matrix = build_normalization_matrix(height, widht, self.shift, self.angle)
        self.update_normalized_coord()

    def set_angle(self, angle) -> None:
        self.angle -= angle

    def get_shift(self) -> Point:
        return self.shift

    def get_center(self) -> Point:
        return self.center
    
    def update_center(self) -> None:
        self.center = Point((self.xmax + self.xmin)/2, (self.ymax + self.ymin)/2)

    def get_display_file(self) -> DisplayFile:
        return self.display_file
    
    def get_xmax(self) -> float:
        return self.xmax
    
    def get_ymax(self) -> float:
        return self.ymax
    
    def get_xmin(self) -> float:
        return self.xmin
    
    def get_ymin(self) -> float:
        return self.ymin
    
    def get_xmax_normalized(self) -> float:
        return self.xmax_normalized
    
    def get_ymax_normalized(self) -> float:
        return self.ymax_normalized
    
    def get_xmin_normalized(self) -> float:
        return self.xmin_normalized
    
    def get_ymin_normalized(self) -> float:
        return self.ymin_normalized
    
    def set_xmax(self, xmax: int) -> None:
        self.xmax = xmax
        self.update_center()
    
    def set_ymax(self, ymax: int) -> None:
        self.ymax = ymax
        self.update_center()

    def set_xmin(self, xmin: int) -> None:
        self.xmin = xmin
        self.update_center()
    
    def set_ymin(self, ymin: int) -> None:
        self.ymin = ymin
        self.update_center()