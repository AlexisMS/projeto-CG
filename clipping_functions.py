from objects import Point

def liang_barsky(point_1: Point, point_2: Point):
    x_min = -1
    y_min = -1
    x_max = 1
    y_max = 1

    x0 = point_1.get_x()
    y0 = point_1.get_y()
    x1 = point_2.get_x()
    y1 = point_2.get_y()

    p1 = -(x1 - x0)
    p2 = -p1
    p3 = -(y1 - y0)
    p4 = -p3

    q1 = x0 - x_min
    q2 = x_max - x0
    q3 = y0 - y_min
    q4 = y_max - y0


    pk = list(zip([p1, p2, p3, p4], [q1, q2, q3, q4]))
    initial_inside_check = any([p == 0 and q < 0 for (p, q) in pk])
    if initial_inside_check:
        return (False, None, None)
    
    r_negative = [(q / p) for (p, q) in pk if p < 0]
    u1 = max(0, max(r_negative, default=0))

    r_positive = [(q / p) for (p, q) in pk if p > 0]
    u2 = min(1, min(r_positive, default=1))

    if u1 > u2:
        return (False, None, None)

    new_x0 = x0 + u1 * p2
    new_y0 = y0 + u1 * p4
    new_x1 = x0 + u2 * p2
    new_y1 = y0 + u2 * p4

    return (True, Point(new_x0, new_y0), Point(new_x1, new_y1))

def nicholl_lee_nicholl(point_1: Point, point_2: Point):
    pass