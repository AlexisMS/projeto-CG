from objects import Point, Point3D
import numpy, math, functools

# ==== OPERAÇÕES 2D ====

def build_normalization_matrix(height:float, widht: float, shift: Point, angle: float) -> numpy.ndarray:
    translation = transform_translate(shift.get_x(), shift.get_y())
    rotation = transform_basic_rotation(angle)
    scaling = transform_basic_scaling(2/widht, 2/height)
    result = functools.reduce(numpy.dot, [translation, rotation, scaling])
    return result

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

# ==== OPERAÇÕES 3D =====

def transform_translate_3d(dx: float, dy: float, dz: float) -> numpy.ndarray:
    translation = numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]])
    return translation

def transform_basic_scaling_3d(sx: float, sy: float, sz: float) -> numpy.ndarray:
    scaling = numpy.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0],[0, 0, 0, 1]])
    return scaling

def transform_scaling_3d(sx: float, sy: float, sz: float, pivot: Point3D) -> numpy.ndarray:
    pivot = pivot
    translation1 = transform_translate_3d(-pivot.get_x(), -pivot.get_y(), -pivot.get_z())
    scaling = transform_basic_scaling_3d(sx, sy, sz)
    translation2 = transform_translate_3d(pivot.get_x(), pivot.get_y(), pivot.get_z())
    result = functools.reduce(numpy.dot, [translation1, scaling, translation2])
    return result

def transform_rotation_3d(angle: float, pivot: Point3D, pivot_angle_x: float, pivot_angle_z: float):
    angle_rad = math.radians(angle)
    pivot_angle_x_rad = math.radians(pivot_angle_x)
    pivot_angle_z_rad = math.radians(pivot_angle_z)
    step1 = transform_translate_3d(-pivot.get_x(), -pivot.get_y(), -pivot.get_z())
    step2 = transform_basic_rotation_3d("x", -pivot_angle_x_rad)
    step3 = transform_basic_rotation_3d("z", -pivot_angle_z_rad)
    step4 = transform_basic_rotation_3d("y", angle_rad)
    step5 = transform_basic_rotation_3d("z", pivot_angle_z_rad)
    step6 = transform_basic_rotation_3d("x", pivot_angle_x_rad)
    step7 = transform_translate_3d(pivot.get_x(), pivot.get_y(), pivot.get_z())
    result = functools.reduce(numpy.dot, [step1, step2, step3, step4, step5, step6, step7])
    return result

def transform_basic_rotation_3d(axis: str, angle: float):
    angle_rad = math.radians(angle)
    if (axis == "x"):
        rotation = numpy.array([[1, 0, 0, 0], [0, math.cos(angle_rad), math.sin(angle_rad), 0], [0, -math.sin(angle_rad), math.cos(angle_rad), 0], [0, 0, 0, 1]])
    elif (axis == "y"):
        rotation = numpy.array([[math.cos(angle_rad), 0, -math.sin(angle_rad), 0], [0, 1, 0, 0], [math.sin(angle_rad), 0, math.cos(angle_rad), 0], [0, 0, 0, 1]])
    elif (axis == "z"):
        rotation = numpy.array([[math.cos(angle_rad), math.sin(angle_rad), 0, 0], [-math.sin(angle_rad), math.cos(angle_rad), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    else:
        rotation = numpy.identity(4)
    return rotation