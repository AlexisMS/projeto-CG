from objects import *

class ObjHandler():
    def __init__(self):
        pass

    def save_file(self, filename: str, target: list[WireFrame]):
        if(not filename.endswith(".obj")):
            filename = filename + ".obj"
        file = open(filename, "x")
        for obj in target:
            points = obj.get_points()
            for p in points:
                file.write("v " + str(p.get_x()) + " " + str(p.get_y()) + " 0.0\n")
            file.write("o " + obj.get_name() + "\n")
            count = int(obj.get_type())
            if count == 1:
                file.write("p -1\n")
            elif count == 2:
                file.write("l -2 -1")
            else:
                file.write("f ")
                while (count > 0):
                    file.write("-" + str(count) + " ")
                    count -= 1
                file.write("\n")
        file.close()

    def open_file(self, filename: str) -> list[WireFrame]:
        if(not filename.endswith(".obj")):
            filename = filename + ".obj"
        file = open(filename, "r")
        objects = []
        points = []
        names = []
        params = []
        for line in file:
            if(line.startswith("o ")):
                split = line.split()
                names.append(split[1])
            elif(line.startswith("v")):
                split = line.split()
                points.append(Point(int(split[1]),int(split[2])))
            elif(line.startswith("p") or line.startswith("l") or line.startswith("f")):
                params.append(line)
        for position, new_obj_name in enumerate(names):
            param = params[position]
            param = param.split()
            param.pop(0)
            obj_points = []
            obj_type = len(param)
            count = obj_type
            while (count > 0):
                obj_points.append(points.pop(0))
                count -= 1
            objects.append(WireFrame(new_obj_name, obj_points))
        file.close()
        return objects