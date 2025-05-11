import pygame, random, copy


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

    def __init__(self, inp=(0,-1), output=(0,1), color=WHITE, function=(lambda x: 2*x, 'mul', 2), cooldown=2):
        image = tools.GFX["machine"]["machine-base"].copy()
        super().__init__(image)
        ObjectInstances.get().machines.append(self)
        Selection.get().draggable.append(self)

        ang = (0, 90, 180, 270)
        inp_angle = random.choice(ang)
        ang2 = list(ang)
        ang2.remove(inp_angle)
        out_angle = random.choice(ang2)

        oper = random.choice(('mul','mul','mul','mul', 'add'))
        if oper == 'mul':
            valu = random.choice((2,3,4,5))
            funcc = lambda x: valu*x
        elif oper == 'add':
            valu = random.randint(2,10)
            funcc = lambda x: valu + x
        function=(funcc, oper, valu)

        cooldown = random.randint(2,5)

        self.input = tools.angle_to_direction(inp_angle)
        self.output = tools.angle_to_direction(out_angle)
        self.__create_rect() # call only once

        self.angle = tools.direction_to_angle(self.input, True)

        rect = pygame.Rect(0,0,46,46)
        rect.center = (SIZE//2, SIZE//2)
        pygame.draw.rect(self.image, color, rect, width=6)

        self.operating = False
        self.occupied = False
        self.function = function[0]
        self.sec_cooldown = cooldown
        self.cooldown = int(cooldown * fps) - fps
        self.__counter = 0
        self.__byte = None

        self.cooldown_surface = pygame.Surface((SIZE,0), flags=pygame.SRCALPHA)

        self.function_text = ''
        if function[1] == 'add':
            self.function_text += '+'
        elif function[1] == 'mul':
            self.function_text += '×'
        self.function_text += f"{function[2]}"

        self.preview = False

    def __repr__(self):
        return '<Mach>'

    @property
    def pos(self):
        return super().pos
    @pos.setter
    def pos(self, xy):
        SpriteObject.pos.fset(self, xy)

    def set_direction(self, angle):
        rotation = self.get_rotation(angle)
        super().set_direction(angle)
        self.input = tools.rotate_direction(self.input, rotation)
        self.output = tools.rotate_direction(self.output, rotation)

    def render(self, screen):
        super().render(screen)
        self.cooldown_surface.fill(pygame.Color(0,0,0,COOLDOWN_ALPHA))
        screen.blit(self.cooldown_surface, self.rect)

    def __create_rect(self):
        # only call once!
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

    def end_round(self):
        self.__byte = None
        self.__counter = 0
        self.operating = False
        self.occupied = False
        self.cooldown_surface = pygame.Surface((SIZE, 0), flags=pygame.SRCALPHA)

    def send_to_storage(self):
        self.pos = (random.randint(SIZE, 300-SIZE), random.randint(300, 700))