import numpy

class Point():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_x(self) -> float:
        return self.x
    
    def get_y(self) -> float:
        return self.y
    
    def set_x(self, x) -> None:
        self.x = x
        
    def set_y(self, y) -> None:
        self.y = y
    
    def get_str_point(self) -> str:
        return "("+str(self.get_x())+","+str(self.get_y())+")"

class WireFrame():
    def __init__(self, name: str, points: list[Point]):
        self.name = name
        self.type = str(len(points))
        self.points = points
        self.normalized_points = []
        self.transform_matrix = numpy.identity(3)
        self.center = self.set_center()

    # Limpa os pontos normalizados
    def clear_normalized_points(self) -> None:
        self.normalized_points.clear()

    # Retorna os pontos normalizados
    def get_normalized_points(self) -> list:
        return self.normalized_points

    # Aplica a normalização dos pontos
    def apply_normalized(self, normalized_matrix) -> None:
        for point in self.points:
            point_matrix = numpy.array([point.get_x(), point.get_y(), 1])
            point_matrix = point_matrix.dot(normalized_matrix)
            normalized_point = Point(point_matrix[0], point_matrix[1])
            self.normalized_points.append(normalized_point)
    
    # Retorna o nome
    def get_name(self) -> str:
        return self.name
    
    # Retorna o tipo
    def get_type(self) -> int:
        return self.type

    # Retorna os pontos
    def get_points(self) -> list:
        return self.points

    # Retorna os pontos em formato printavel
    def get_str_points(self) -> str:
        str_point = ""
        for p in self.points:
            str_point += "("+str(p.get_x())+","+str(p.get_y())+")"
        return str_point
    
    # Define o centro
    def set_center(self) -> Point:
        xsum = 0
        ysum = 0
        for point in self.points:
            xsum = xsum + point.get_x()
            ysum = ysum + point.get_y()
        x = xsum/len(self.points)
        y = ysum/len(self.points)
        self.center = Point(x, y)
        return Point(x, y)
    
    # Retorna o centro
    def get_center(self) -> Point:
        return self.center
    
    # Retorna a matriz de transformação
    def get_transform(self) -> numpy.ndarray:
        return self.transform_matrix
    
    # Atualiza a matriz de transformação
    def update_transform(self, matrix: numpy.ndarray) -> None:
        self.transform_matrix = self.transform_matrix.dot(matrix)

    # Reseta a matriz de transformação
    def reset_transform(self) -> None:
        self.transform_matrix = numpy.identity(3)
    
    # Aplica a matriz de transformação
    def apply_transform(self) -> None: # lembrete de rodar reset_transform() depois
        for point in self.points:
            point_matrix = numpy.array([point.get_x(), point.get_y(), 1])
            point_matrix = point_matrix.dot(self.transform_matrix)
            point.set_x(point_matrix[0])
            point.set_y(point_matrix[1])
        self.set_center()

class Segment_Curva2D_bezier(WireFrame):
    def __init__(self, ctrl_points: list[Point], steps: int):
        self.type = "curve"
        self.ctrl_points = ctrl_points
        self.mb = numpy.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]) # definição de bezier
        self.gbx = numpy.array([[ctrl_points[0].get_x()], [ctrl_points[1].get_x()], [ctrl_points[2].get_x()], [ctrl_points[3].get_x()]])
        self.gby = numpy.array([[ctrl_points[0].get_y()], [ctrl_points[1].get_y()], [ctrl_points[2].get_y()], [ctrl_points[3].get_y()]])
        self.points = []
        for i in range(steps+1):
            point = self.set_point(i/steps)
            self.points.append(point)
    
    def set_point(self, t: float) -> Point:
        t_array = numpy.array([pow(t,3), pow(t,2), t, 1])
        temp = numpy.matmul(t_array, self.mb)
        return Point(numpy.matmul(temp, self.gbx)[0], numpy.matmul(temp, self.gby)[0])

class Curva2D_bezier(WireFrame):
    def __init__(self, name: str, ctrl_points: list[Point], steps: int):
        self.name = name
        self.ctrl_points = ctrl_points
        self.points = []
        self.normalized_points = []
        self.type = "curve"
        while(1):
            curve_segment = Segment_Curva2D_bezier([ctrl_points[0], ctrl_points[1], ctrl_points[2], ctrl_points[3]], steps)
            self.points = self.points + curve_segment.get_points()
            ctrl_points = ctrl_points[3:]
            if len(ctrl_points)<4:
                break
        for p in self.points:
            print(type(p), p.get_str_point())
        self.transform_matrix = numpy.identity(3)
        self.center = self.set_center()

class Curva2D_fwd_diff(WireFrame):
    def __init__(self, name: str, ctrl_points: list[Point]):
        # similar ao curva2D_bezier, usa o segment_curva2d_fwd_diff pra ir criando segmentos usando 4 pontos por vez
        # aceita qualquer número de pontos igual ou maior que 4
        pass

class Segment_Curva2D_fwd_diff(WireFrame):
    def __init__(self, name: str, ctrl_points: list[Point]): # aceita especificamente 4 pontos
        self.name = name
        self.ctrl_points = ctrl_points
        self.points = []
        self.normalized_points = []
        self.type = "curve"
        # calcular coeficientes a, b, c, d para x e y, usando C=Mbs*Gbs
        Mbs = numpy.array([[2, -2, 1, 1],[-3, 3, -2, 1],[0, 0, 1, 0],[1, 0, 0, 0]])
        # Gbsx = [[P1x],[P4x],[R1x],[R4x]]
        # Gbsy = [[P1y],[P4y],[R1y],[R4y]]
        # definir delta (arbitrário)
        # valores para o primeiro ponto:
        # f0 = d
        # df0 = a*delta^3 + b*delta^2 + c*delta
        # d2f0 = 6*a*delta^3 + 2*b*delta^2
        # d3f0 = 6*a*delta^3
        # chamar fwd_diff para gerar os outros pontos da curva

    def fwd_diff(self, n, x, dx, d2x, d3x, y, dy, d2y, d3y): #, z, dz, d2z, d3z):
        i = 1
        x_old = x
        y_old = y
        #z_old = z
        while(i<n):
            i += 1
            x += dx
            dx += d2x
            d2x += d3x
            y += dy
            dy += d2y
            d2y += d3y
            #z += dz
            #dz += d2z
            #d2z += d3z
            self.points.append(Point(x_old, y_old))
            self.points.append(Point(x, y))
            x_old = x
            y_old = y
            #z_old = z
