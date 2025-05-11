import pygame, math, colorsys

from data.base.instances import ObjectInstances
from data.base.object import RectObject, TextObject
from data.base.conveyor import Conveyor
from data.base.machine import Machine
from data.config import SIZE, fps, color_light1, color_dark1, WHITE
from data import tools


class Byte(RectObject):
    __instances = []
    __MAX = 1000000

    @staticmethod
    def instances():
        return Byte.__instances

    def __init__(self):
        ObjectInstances.get().bytes.append(self)

        rect = pygame.Rect(0, 0, 50, 50)
        super().__init__(rect, color_dark1)
        self.direction = (0,0)
        self.__pos = [0,0]
        self.__bytes = 1
        self.__text = TextObject(str(self.__bytes),32,WHITE)
        self.__current_square = None
        self.__check_new = False
        self.__set_byte(self.__bytes)
        self.__paused = False
        self.__operating = False
        self.__scored = False

    @property
    def pos(self):
        return super().pos
    @pos.setter
    def pos(self, pos):
        RectObject.pos.fset(self, pos)
        self.__text.center = self.pos

    @property
    def byte(self):
        return self.__bytes

    def __set_byte(self, val):
        self.__bytes = val
        x = math.log(self.__bytes, Byte.__MAX) # ∈[0,1]
        self.__text.color = [x * 255 for x in colorsys.hsv_to_rgb(x, 0.5 + x/2, 0.8)]
        self.__text.text = str(int(val))

    def __get_color(self):
        math.log(self.__bytes, 10)

    def render(self, screen):
        if not self.__scored:
            pygame.draw.rect(screen, color_light1, self.rect, border_radius=10)
            pygame.draw.rect(screen, self.color, self.rect, width=4, border_radius=10)
            self.__text.render(screen)

    def update_loop(self, grid, info):
        if not self.__scored:
            if grid.in_grid(self.pos):
                if self.__current_square is None:
                    self.__current_square = grid.get_square(self.pos)

                if self.__paused:
                    obj = grid.object_at(self.pos)
                    if isinstance(obj, Machine): # technically should not be necessary
                        if not obj.occupied:
                            self.__paused = False
                else:
                    self.pos = (self.pos[0] + (SIZE / fps * self.direction[0]),
                                self.pos[1] + (SIZE / fps * self.direction[1]))
                new_square = grid.get_square(self.pos)

                if new_square != self.__current_square:
                    self.__check_new = True
                    if not self.__paused:
                        self.__current_square = new_square
                if not self.__paused and self.__check_new and grid.in_grid(self.pos):
                    self.__check_new = False
                    new_object = grid.data[new_square[1]][new_square[0]]
                    if new_object != "None" and not isinstance(new_object, Conveyor):
                        if isinstance(new_object, Machine):
                            if new_object.valid_input(self.direction):
                                if new_object.occupied:
                                    self.__paused = True
                                    self.__check_new = True
                                else:
                                    new_object.occupied = True
                            else:
                                self.direction = (0, 0)
                        else:
                            self.direction = (0, 0)

                center = grid.snap_pos(self.pos)
                if center[0] - 1 <= self.pos[0] <= center[0] + 1 and center[1] - 1 <= self.pos[1] <= center[1] + 1:
                    col, row = grid.get_square(self.pos)
                    obj = grid.data[row][col]
                    if obj == 'None':
                        self.direction = (0, 0)
                    elif isinstance(obj, Conveyor):
                        conv = obj
                        self.direction = tools.angle_to_direction(conv.angle)
                    elif isinstance(obj, Machine) and not self.__operating:
                        # There should be no need to check for correct input or occupied status if it made it to this point.
                        self.__operating = True
                        obj.operate_byte(self)
            else:
                if self.pos[0] > grid.bound_pos[0]:
                    self.__scored = True
                    info.round_progress += self.__bytes


    def done(self):
        self.__operating = False

    def apply(self, func):
        self.__set_byte(func(self.__bytes))

    @staticmethod
    def render_all(screen):
        for i in Byte.__instances:
            i.render(screen)