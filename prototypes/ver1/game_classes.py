import pygame
from config2 import Config as cf
from game_display import Display


class GameManager:
    active_scene = None

class Scene:
    __active_scene = None

    @staticmethod
    def active():
        return Scene.__active_scene

    @staticmethod
    def set_to(scene):
        Scene.__active_scene = scene

    def __init__(self):
        self.sprites = []
        self.draggable = [] # check only draggable objects
        self.dragging = []

class GameInfo:
    text = []
    draggable = []
    dragging = []
    drag_xy = []
    display = Display()

class RectObject:
    def __init__(self, rect=None, color=(0,0,0)):
        if rect is None:
            self.rect = pygame.Rect(0,0,0,0)
        else:
            self.rect = rect
        self.color = color
        self.radius = 0
        GameInfo.rects.append(self)

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.surface = pygame.image.load(image)
        self.rect = self.surface.get_rect()
        self.rect.center = (x, y)

class GameObject:
    def __init__(self, surface=None, color='magenta', z_order=None):
        if surface is None:
            self.surface = pygame.Surface((80,80))
        else:
            self.surface = surface
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        if z_order is None:
            self.__z = GameInfo.display.top() +  1
        else:
            self.__z = z_order
        GameInfo.display.add(self)

    def resurface(self, surface):
        self.surface = surface
        self.rect = self.surface.get_rect()

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def xy(self):
        return self.rect.x, self.rect.y
    @xy.setter
    def xy(self, value):
        self.rect.x = value[0]
        self.rect.y = value[1]

    @property
    def z(self):
        return self.__z
    @z.setter
    def z(self, z):
        self.__z = z
        GameInfo.display.reorder(self)

    def render(self, screen):
        screen.blit(self.surface, self.rect)

    '''def move_x(self, x):
        self.x += x
        self.xy[0] += x
    def move_y(self, y):
        self.y += y
        self.xy[1] += y
    def move(self, xy):
        self.move_x(xy[0])
        self.move_y(xy[1])
        self.rect.move_ip(xy)'''

class SpriteObject:
    def __init__(self, surface=None):
        if surface is None:
            self.surface = pygame.Surface((80,80))
            self.surface.fill('magenta')
        self.rect = self.surface.get_rect()

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def xy(self):
        return self.rect.x, self.rect.y
    @xy.setter
    def xy(self, value):
        self.rect.x = value[0]
        self.rect.y = value[1]

class DraggableObject(GameObject):
    def __init__(self):
        super().__init__()
        GameInfo.draggable.append(self)

class Byte(GameObject):
    def __init__(self):
        super().__init__()
        self.byte = 1

    def apply(self, func):
        self.byte = func(self.byte)

class Machine(DraggableObject):
    def  __init__(self, size):
        super().__init__()
        self.size = size

class Grid(GameObject):
    def __init__(self, size=(3,3)):
        super().__init__()
        self.surface = pygame.Surface((0,0))
        self.rect = pygame.Rect(0,0,0,0)
        self.size = list(size)
        self.grid_line_width = 6
        self.square_size = 80

        self.x = 800
        self.y = cf.window_height // 2
        self.__calculate_bound()

    @GameObject.x.setter
    def x(self, value):
        self.rect.x = value
        self.__calculate_bound()
    @GameObject.y.setter
    def y(self, value):
        self.rect.y = value
        self.__calculate_bound()
    @GameObject.xy.setter
    def xy(self, value):
        self.rect.x = value[0]
        self.rect.y = value[1]
        self.__calculate_bound()

    def __calculate_bound(self):
        self.x_bound = self.x + self.square_size * self.size[0]
        self.y_bound = self.y + self.square_size * self.size[1]

    def snap(self, object):
        if (self.x < pygame.mouse.get_pos()[0] < self.x_bound and
            self.y < pygame.mouse.get_pos()[1] < self.y_bound and
            object in GameInfo.dragging):
            col = (pygame.mouse.get_pos()[0] - self.x) // self.square_size
            row = (pygame.mouse.get_pos()[1] - self.y) // self.square_size
            object.xy = [self.x + self.square_size*col + self.grid_line_width//2,
                         self.y + self.square_size*row + self.grid_line_width//2]

    def render(self, screen):
        pygame.draw.rect(screen, cf.grid_background, pygame.Rect(self.x, self.y, self.square_size*self.size[0],
                                                                 self.square_size*self.size[1]))
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                tmp = pygame.Rect(self.x + self.square_size*i, self.y + self.square_size*j,
                                  self.square_size+self.grid_line_width, self.square_size+self.grid_line_width)
                pygame.draw.rect(screen, cf.grid_line, tmp, self.grid_line_width)

    def center(self, xy):
        self.xy = xy
        self.x = self.x - self.square_size * self.size[0] // 2
        self.y = self.y - self.square_size * self.size[1] // 2

    def grow(self, side):
        if side == 0:
            self.size[0] += 1
        elif side == 1:
            self.size[1] += 1
        self.__calculate_bound()

class Conveyor(GameObject):
    def __init__(self):
        pass