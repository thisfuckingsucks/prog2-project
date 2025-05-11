import pygame.mouse


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

    def update_loop(self, grid, info, timer):
        for b in self.bytes:
            b.update_loop(grid, info)
        for m in self.machines:
            m.update_loop()
        for g in self.generators:
            g.update_loop(grid, timer)

    def update_direction(self, angle, grid):
        for m in self.machines:
            if not grid.part_of_grid(m):
                m.set_direction(angle)
        for g in self.generators:
            if not grid.part_of_grid(g):
                g.set_direction(angle)

    def end_round(self):
        for m in self.machines:
            m.end_round()
        self.bytes.clear()