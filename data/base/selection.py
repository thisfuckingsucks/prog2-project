

class Selection:
    __instance = None

    @staticmethod
    def get():
        return Selection.__instance

    def __init__(self):
        self.draggable = []
        self.current_dragging = []

        self.place_direction = 270

        Selection.__instance = self

    def get_direction(self):
        return self.place_direction