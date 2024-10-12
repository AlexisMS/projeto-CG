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
        self.update_normalization_matrix()

    # Retorna a matriz de normalização
    def get_normalization_matrix(self) -> numpy.ndarray:
        return self.normalization_matrix

    # Atualiza a matriz de normalização
    def update_normalization_matrix(self) -> None:
        height = self.ymax - self.ymin
        widht = self.xmax - self.xmin
        self.normalization_matrix = build_normalization_matrix(height, widht, self.shift, self.angle)

    # Defino o ângulo de rotação
    def set_angle(self, angle) -> None:
        self.angle -= angle

    # Retorna o deslocamento
    def get_shift(self) -> Point:
        return self.shift

    # Retorna o centro
    def get_center(self) -> Point:
        return self.center
    
    # Atualiza o centro
    def update_center(self) -> None:
        self.center = Point((self.xmax + self.xmin)/2, (self.ymax + self.ymin)/2)

    # Retorna o display file
    def get_display_file(self) -> DisplayFile:
        return self.display_file
    
    # Retorna o x maximo
    def get_xmax(self) -> float:
        return self.xmax
    
    # Retorna o y maximo
    def get_ymax(self) -> float:
        return self.ymax
    
    # Retorna o x minimo
    def get_xmin(self) -> float:
        return self.xmin
    
    # Retorna o y minimo
    def get_ymin(self) -> float:
        return self.ymin
    
    # Define o x maximo
    def set_xmax(self, xmax: int) -> None:
        self.xmax = xmax

    # Define o y maximo
    def set_ymax(self, ymax: int) -> None:
        self.ymax = ymax

    # Define o x minimo
    def set_xmin(self, xmin: int) -> None:
        self.xmin = xmin
    
    # Define o y minimo
    def set_ymin(self, ymin: int) -> None:
        self.ymin = ymin
