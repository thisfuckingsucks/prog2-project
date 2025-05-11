



class ObjectInstances:
    __instance = None

    @staticmethod
    def get():
        return ObjectInstances.__instance

    def __init__(self):
        ObjectInstances.__instance = self

        self.bytes = []
        self.machines = []
        self.generators = []
        self.conveyors = []

    def render(self, screen):
        for i in self.conveyors:
            i.render(screen)
        for i in self.generators:
            i.render(screen)
        for i in self.machines:
            i.render(screen)
        for i in self.bytes:
            i.render(screen)

    def update_loop(self, grid):
        for b in self.bytes:
            b.update_loop()
        for m in self.machines:
            m.update_loop()
        for g in self.generators:
            g.update_loop(grid)