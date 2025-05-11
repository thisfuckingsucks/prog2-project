import pygame, copy

#from data.config import conveyor_sprites
from data.base.instances import ObjectInstances
from data.base.object import AnimatedSpriteObject
from data.base.timer import Timer
from data import tools

sheet = tools.GFX["conveyor"]
conveyor_sprites = (sheet["conveyor1"],sheet["conveyor2"],sheet["conveyor3"],sheet["conveyor4"],sheet["conveyor5"],
                    sheet["conveyor6"],sheet["conveyor7"],sheet["conveyor8"],sheet["conveyor9"],sheet["conveyor10"])

class Conveyor(AnimatedSpriteObject):
    __instances = []

    def __init__(self, pos, angle=270):
        super().__init__(conveyor_sprites)
        self.pos = pos
        self.speed = 1
        self.set_direction(angle)

        #Conveyor.__instances.append(self)
        ObjectInstances.get().conveyors.append(self)

    def __repr__(self):
        return 'Cnvyer'

    def update(self):
        self.current = Timer.get_animation_time() % 10
        self.image = self.sprites[self.current]

    @staticmethod
    def render_all(screen):
        for i in Conveyor.__instances:
            i.render(screen)