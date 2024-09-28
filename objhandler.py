from objects import *

class ObjHander():
    def __init__():
        pass

    def save_file(filename: str, target: list[WireFrame]):
        if(not filename.endswith(".obj")):
            filename = filename + ".obj"
        file = open(filename, "x")
        for obj in target:
            points = obj.get_points()
            for p in points:
                file.write("v " + str(p.get_x()) + " " + str(p.get_y()) + " 0.0\n")
            file.write("o " + obj.get_name() + "\n")
            count = obj.get_type()
            if count == 1:
                file.write("p -1\n")
            else:
                file.write("f ")
                while (count > 0):
                    file.write("-" + str(count) + " ")
                    count -= 1
                file.write("\n")
        file.close()

    def open_file(filename: str):
        if(not filename.endswith(".obj")):
            filename = filename + ".obj"
        file = open(filename, "a")

        file.close()