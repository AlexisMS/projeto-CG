from display_file import DisplayFile
from objects import Point


class Window():
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int, display_file: DisplayFile):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.center = Point((xmax + xmin)/2, (ymax + ymin)/2)
        self.display_file = display_file
        self.zoom = 0

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
