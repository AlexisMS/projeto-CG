from objects import Point

def liang_barsky(point_1: Point, point_2: Point):
    x_min = -1
    y_min = -1
    x_max = 1
    y_max = 1

    x0, y0 = point_1
    x1, y1 = point_2

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

def cohen_sutherland(point_1: Point, point_2: Point):
    p1_rc = [(point_1.get_y()>1), (point_1.get_y()<-1), (point_1.get_x()>1), (point_1.get_x()<-1)]
    p2_rc = [(point_2.get_y()>1), (point_2.get_y()<-1), (point_2.get_x()>1), (point_2.get_x()<-1)]
    and_rc = [(p1_rc[0] and p2_rc[0]), (p1_rc[1] and p2_rc[1]), (p1_rc[2] and p2_rc[2]), (p1_rc[3] and p2_rc[3])]
    m = (point_2.get_y() - point_1.get_y())/(point_2.get_x() - point_1.get_x())

    if p1_rc == p2_rc and p1_rc == [False, False, False, False]:
        return(True, point_1, point_2)
    elif and_rc != [False, False, False, False]:
        return(False, None, None)
    elif p1_rc != p2_rc and and_rc == [False, False, False, False]:
        if p1_rc == [False, False, False, False]:
            new_p1 = point_1
            # clipa ponto 2
            if p2_rc[0] == True:
                if m == 0:
                    new_x = point_2.get_x()
                else:                    
                    new_x =  point_2.get_x() + (1/m)*(1-point_2.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p2 = Point(new_x, 1)
                else:
                    return(False, None, None)
            elif p2_rc[1] == True:
                if m == 0:
                    new_x = point_2.get_x()
                else:                    
                    new_x =  point_2.get_x() + (1/m)*((-1)-point_2.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p2 = Point(new_x, -1)
                else:
                    return(False, None, None)
            elif p2_rc[2] == True:
                if m == 0:
                    new_y = point_2.get_y()
                else:                    
                    new_y =  m*(1-point_2.get_x()) + point_2.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p2 = Point(1, new_y)
                else:
                    return(False, None, None)
            elif p2_rc[3] == True:
                if m == 0:
                    new_y = point_2.get_y()
                else:                    
                    new_y =  m*((-1)-point_2.get_x()) + point_2.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p2 = Point(-1, new_y)
                else:
                    return(False, None, None)
        elif p2_rc == [False, False, False, False]:
            new_p2 = point_2
            # clipa ponto 1
            if p1_rc[0] == True:
                if m == 0:
                    new_x = point_1.get_x()
                else:                    
                    new_x =  point_1.get_x() + (1/m)*(1-point_1.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p1 = Point(new_x, 1)
                else:
                    return(False, None, None)
            elif p1_rc[1] == True:
                if m == 0:
                    new_x = point_1.get_x()
                else:                    
                    new_x =  point_1.get_x() + (1/m)*((-1)-point_1.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p1 = Point(new_x, -1)
                else:
                    return(False, None, None)
            elif p1_rc[2] == True:
                if m == 0:
                    new_y = point_1.get_y()
                else:                    
                    new_y =  m*(1-point_1.get_x()) + point_1.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p1 = Point(1, new_y)
                else:
                    return(False, None, None)
            elif p1_rc[3] == True:
                if m == 0:
                    new_y = point_1.get_y()
                else:                    
                    new_y =  m*((-1)-point_1.get_x()) + point_1.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p1 = Point(-1, new_y)
                else:
                    return(False, None, None)
        else:
            # clipa os dois pontos
            if p1_rc[0] == True:
                if m == 0:
                    new_x = point_1.get_x()
                else:                    
                    new_x =  point_1.get_x() + (1/m)*(1-point_1.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p1 = Point(new_x, 1)
                else:
                    return(False, None, None)
            elif p1_rc[1] == True:
                if m == 0:
                    new_x = point_1.get_x()
                else:                    
                    new_x =  point_1.get_x() + (1/m)*((-1)-point_1.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p1 = Point(new_x, -1)
                else:
                    return(False, None, None)
            elif p1_rc[2] == True:
                if m == 0:
                    new_y = point_1.get_y()
                else:                    
                    new_y =  m*(1-point_1.get_x()) + point_1.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p1 = Point(1, new_y)
                else:
                    return(False, None, None)
            elif p1_rc[3] == True:
                if m == 0:
                    new_y = point_1.get_y()
                else:                    
                    new_y =  m*((-1)-point_1.get_x()) + point_1.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p1 = Point(-1, new_y)
                else:
                    return(False, None, None)
            if p2_rc[0] == True:
                if m == 0:
                    new_x = point_2.get_x()
                else:                    
                    new_x =  point_2.get_x() + (1/m)*(1-point_2.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p2 = Point(new_x, 1)
                else:
                    return(False, None, None)
            elif p2_rc[1] == True:
                if m == 0:
                    new_x = point_2.get_x()
                else:                    
                    new_x =  point_2.get_x() + (1/m)*((-1)-point_2.get_y())
                if new_x > -1 and new_x < 1:                    
                    new_p2 = Point(new_x, -1)
                else:
                    return(False, None, None)
            elif p2_rc[2] == True:
                if m == 0:
                    new_y = point_2.get_y()
                else:                    
                    new_y =  m*(1-point_2.get_x()) + point_2.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p2 = Point(1, new_y)
                else:
                    return(False, None, None)
            elif p2_rc[3] == True:
                if m == 0:
                    new_y = point_2.get_y()
                else:                    
                    new_y =  m*((-1)-point_2.get_x()) + point_2.get_y()
                if new_y > -1 and new_y < 1:                    
                    new_p2 = Point(-1, new_y)
                else:
                    return(False, None, None)
        return(True, new_p1, new_p2)
    else:
        return(False, None, None)