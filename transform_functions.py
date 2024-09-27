from objects import Point
import numpy, math, functools


def transform_scaling(sx: float, sy: float, pivot: Point) -> numpy.ndarray:
    pivot = pivot
    translation1 = transform_translate(-pivot.get_x(), -pivot.get_y())
    scaling = transform_basic_scaling(sx, sy)
    translation2 = transform_translate(pivot.get_x(), pivot.get_y())
    result = functools.reduce(numpy.dot, [translation1, scaling, translation2])
    return result
    
def transform_rotation(angle: float, pivot: Point) -> numpy.ndarray:
    translation1 = transform_translate(-pivot.get_x(), -pivot.get_y())
    rotation = transform_basic_rotation(angle)
    translation2 = transform_translate(pivot.get_x(), pivot.get_y())
    result = functools.reduce(numpy.dot, [translation1, rotation, translation2])
    return result

def transform_translate(dx: float, dy: float) -> numpy.ndarray:
    translation = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
    return translation

def transform_basic_scaling(sx: float, sy: float) -> numpy.ndarray:
    scaling = numpy.array([[sx, 0, 0],[0, sy, 0],[0, 0, 1]])
    return scaling

def transform_basic_rotation(angle: float) -> numpy.ndarray:
    angle_rad = math.radians(angle)
    rotation = numpy.array([[math.cos(angle_rad), -math.sin(angle_rad), 0],[math.sin(angle_rad),math.cos(angle_rad),0],[0, 0, 1]])
    return rotation
