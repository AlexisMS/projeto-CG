from objects import *

class ObjHander():
    def __init__():
        pass

    def new_file(self, filename: str):
        if(not filename.endswith(".obj")):
            filename = filename + ".obj"
        self.file = open(filename, "a")

    def add_obj_to_file(self, target: WireFrame):
        if(self.file):
            points = target.get_points()
            for p in points:
                self.file.write("v " + str(p.get_x()) + " " + str(p.get_y()) + " 0.0\n")
            self.file.write("o " + target.get_name() + "\n")
            count = target.get_type()
            if count == 1:
                self.file.write("p -1\n")
            else:
                self.file.write("f ")
                while (count > 0):
                    self.file.write("-" + str(count) + " ")
                    count -= 1
                self.file.write("\n")

    def close_file(self):
        if(self.file):
            self.file.close()

    def open_file():
        pass