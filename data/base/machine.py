import pygame


from data.base.instances import ObjectInstances
from data.base.object import SpriteObject
from data.base.selection import Selection
from data.config import input_blue, output_red, SIZE, WHITE, fps, COOLDOWN_ALPHA
from data import tools


class Machine(SpriteObject):
    __instances = []

    @staticmethod
    def instances():
        return Machine.__instances

    def __init__(self, inp=(0,-1), output=(0,1), color=WHITE, function=lambda x: 2*x, cooldown=2):
        image = tools.GFX["machine"]["machine-base"]
        super().__init__(image)
        ObjectInstances.get().machines.append(self)
        Selection.get().draggable.append(self)

        self.input = inp
        self.output = output
        self.create_rect()

        rect = pygame.Rect(0,0,46,46)
        rect.center = (SIZE//2, SIZE//2)
        pygame.draw.rect(self.image, color, rect, width=6)

        self.operating = False
        self.occupied = False
        self.function = function
        self.cooldown = int(cooldown * fps) - fps
        self.__counter = 0
        self.__byte = None

        self.cooldown_surface = pygame.Surface((SIZE,0), flags=pygame.SRCALPHA)

    def __repr__(self):
        return '<Mach>'

    @property
    def pos(self):
        return super().pos
    @pos.setter
    def pos(self, xy):
        SpriteObject.pos.fset(self, xy)

    def render(self, screen):
        super().render(screen)
        self.cooldown_surface.fill(pygame.Color(0,0,0,COOLDOWN_ALPHA))
        screen.blit(self.cooldown_surface, self.rect)

    def create_rect(self):
        rect = None

        if self.input[0] == 0:
            rect = pygame.Rect(0,0,60,10)
            rect.center = (SIZE//2, SIZE//2 + 35*self.input[1])
        elif self.input[1] == 0:
            rect = pygame.Rect(0, 0, 10, 60)
            rect.center = (SIZE // 2 + 35 * self.input[0], SIZE//2)
        pygame.draw.rect(self.image, input_blue, rect)

        if self.output[0] == 0:
            rect = pygame.Rect(0,0,60,10)
            rect.center = (SIZE//2, SIZE//2 + 35*self.output[1])
        elif self.output[1] == 0:
            rect = pygame.Rect(0, 0, 10, 60)
            rect.center = (SIZE // 2 + 35 * self.output[0], SIZE//2)
        pygame.draw.rect(self.image, output_red, rect)

    def start_cooldown(self):
        self.__counter = self.cooldown
        self.cooldown_surface = pygame.Surface((SIZE,SIZE), flags=pygame.SRCALPHA)
        #self.cooldown_rect.topleft = self.rect.topleft

    def update_loop(self):
        #print(self.cooldown_surface.get_height())
        if self.__counter > 0:
            self.__counter -= 1
            self.cooldown_surface = pygame.Surface((SIZE, int(SIZE * (self.__counter/self.cooldown))),
                                                   flags=pygame.SRCALPHA)
            # print(f"machine : {self.__counter}  ", end='')
        if self.operating:
            if self.__counter == 0:
                self.operating = False
                self.occupied = False
                self.__byte.apply(self.function)
                self.__byte.done()
                self.__byte.direction = self.output
                self.cooldown_surface = pygame.Surface((SIZE, 0), flags=pygame.SRCALPHA)

    def valid_input(self, direction):
        return list(direction) == [-1 * x for x in self.input]

    def operate_byte(self, byte):
        byte.direction = (0,0)
        self.start_cooldown()
        self.operating = True
        self.__byte = byte