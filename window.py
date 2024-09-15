from display_file import DisplayFile


class Window():
    def __init__(self, x: int, y: int, display_file: DisplayFile):
        self.x = x
        self.y = y
        self.display_file = display_file


    def get_display_file(self) -> DisplayFile:
        return self.display_file
    
    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y
    
    def set_x(self, x: int) -> None:
        self.x = x
    
    def set_y(self, y: int) -> None:
        self.y = y