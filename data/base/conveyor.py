import pygame, copy

#from data.config import conveyor_sprites

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

        Conveyor.__instances.append(self)

    def __repr__(self):
        return 'Cnvyer'

    def update(self):
        self.current = Timer.get_time() % 10
        self.image = self.sprites[self.current]

    """def __update_direction(self, x):
        if x == (1,0): angle = 90
        elif x == (0,-1): angle = 180
        elif x == (-1,0): angle = 270
        else: angle = 0
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.rotate(self.sprites[i], angle)
        self.direction = x
        print(angle)"""

    @staticmethod
    def render_all(screen):
        for i in Conveyor.__instances:
            i.render(screen)