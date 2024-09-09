class WireFrame():
    def __init__(self, name = str, points = list):
        self.name = name
        self.type = str(len(points))
        self.points = points.copy()

    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

    def get_points(self):
        return self.points
    
    def get_str_points(self):
        str_point = ""
        
        for p in self.points:
            str_point += "("+str(p.x())+","+str(p.y())+")"
            
        return str_point