class WireFrame():
    def __init__(self, name = str, points = list):
        self.name = name
        self.type = str(len(points))
        self.points = points

    def get_name(self) -> str:
        return self.name
    
    def get_type(self) -> int:
        return self.type

    def get_points(self) -> list:
        return self.points
    
    def get_str_points(self) -> str:
        str_point = ""
        
        for p in self.points:
            str_point += "("+str(p.get_x())+","+str(p.get_y())+")"
            
        return str_point
    

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y