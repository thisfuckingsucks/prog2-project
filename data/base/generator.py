import pygame

from data.base.instances import ObjectInstances
from data.base.object import SpriteObject, TextObject
from data.base.selection import Selection
from data.base import conveyor, timer, byte
from data import tools, config



class Generator(SpriteObject):
    __instances = []

    def __init__(self):
        image = tools.GFX["generator"]["generator1"]
        super().__init__(image)
        self._text = TextObject("+1", 48, color=config.WHITE)
        self.output = (0,1)

        Selection.get().draggable.append(self)
        ObjectInstances.get().generators.append(self)

    @property
    def pos(self):
        return super().pos
    @pos.setter
    def pos(self, pos):
        SpriteObject.pos.fset(self, pos)
        self._text.center = self.pos


    def render(self, screen):
        super().render(screen)
        self._text.render(screen)

    def update_loop(self, grid):
        if grid.part_of_grid(self):
            # print(f"generator : {timer.Timer.get_time()%120}")
            if timer.Timer.get_time()%120 == 0:
                if grid.check_square(self, conveyor.Conveyor, self.output):
                    b = byte.Byte()
                    b.pos = self.pos
                    b.direction = tools.angle_to_direction(self.angle)