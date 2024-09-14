from display_file import DisplayFile


class Window():
    def __init__(self, x, y, display_file = DisplayFile):
        self.x = x
        self.y = y
        self.display_file = display_file


    def get_display_file(self) -> DisplayFile:
        return self.display_file