from objects import WireFrame


class DisplayFile():
    def __init__(self):
        self.objects = []

    def add_object(self, object = WireFrame) -> None:
        self.objects.append(object)
    
    def get_objects(self) -> list[WireFrame]:
        return self.objects