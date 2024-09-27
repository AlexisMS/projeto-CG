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
        self.shift = Point(0,0)
        self.center = Point((xmax + xmin)/2, (ymax + ymin)/2)
        self.display_file = display_file
        self.normalization_matrix = numpy.identity(3)
        self.angle = 0
        self.zoom = 0

    def get_normalization_matrix(self) -> numpy.ndarray:
        return self.normalization_matrix

    def update_normalization_matrix(self) -> None:
        height = self.ymax - self.ymin
        widht = self.xmax - self.xmin
        self.normalization_matrix = build_normalization_matrix(height, widht, self.shift, self.angle)

    def set_angle(self, angle):
        self.angle -= angle

    def get_shift(self) -> Point:
        return self.shift

    def get_center(self) -> Point:
        return self.center
    
    def update_center(self) -> None:
        self.center = Point((self.xmax + self.xmin)/2, (self.ymax + self.ymin)/2)

    def get_display_file(self) -> DisplayFile:
        return self.display_file
    
    def get_xmax(self) -> int:
        return self.xmax
    
    def get_ymax(self) -> int:
        return self.ymax
    
    def get_xmin(self) -> int:
        return self.xmin
    
    def get_ymin(self) -> int:
        return self.ymin
    
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
