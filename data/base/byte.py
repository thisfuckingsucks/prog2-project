import pygame, math

from data.base.object import RectObject
from data.base.grid import Grid
from data.base.conveyor import Conveyor
from data.config import SIZE, fps, color_light1, color_dark1


class Byte(RectObject):
    __instances = []

    @staticmethod
    def instances():
        return Byte.__instances

    def __init__(self):
        rect = pygame.Rect(0, 0, 50, 50)
        super().__init__(rect, color_dark1)
        self.direction = (0,0)
        self.__pos = [0,0]
        #Scene.active().info.bytes.append(self)
        Byte.__instances.append(self)

    def render(self, screen):
        pygame.draw.rect(screen, color_light1, self._rect, border_radius=10)
        pygame.draw.rect(screen, self.color, self._rect, width=4, border_radius=10)

    def update_loop(self):
        grid = Grid.instance()
        if grid.in_grid(self.pos):
            self.pos = (self.pos[0] + (SIZE / fps * self.direction[0]),
                        self.pos[1] + (SIZE / fps * self.direction[1]))

            center = grid.snap_pos(self.pos)
            if center[0] - 1 <= self.pos[0] <= center[0] + 1 and center[1] - 1 <= self.pos[1] <= center[1] + 1:
                col, row = grid.get_square(self.pos)
                obj = grid.data[row][col]
                if obj == 'None':
                    self.direction = (0, 0)
                elif isinstance(obj, Conveyor):
                    conv = obj
                    self.direction = (math.cos(math.radians(conv.angle)),
                                      - math.sin(math.radians(conv.angle)))

    @staticmethod
    def render_all(screen):
        for i in Byte.__instances:
            i.render(screen)