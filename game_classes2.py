import pygame
from config import Config as cf


class Scene:
    __active_scene = None
    __scenes = {}

    @staticmethod
    def active():
        return Scene.__active_scene

    @staticmethod
    def set_to(scene):
        Scene.__active_scene = scene

    @staticmethod
    def get(scene: str):
        return Scene.__scenes[scene]

    def __init__(self, scene: str):
        self.__scene = scene
        self.__render = []
        self.sprites = []
        self.draggable = [] # check only draggable objects
        self.dragging = []
        self.mode = 'None'
        self.components = {}
        Scene.__scenes[scene] = self

    def add_render(self, r):
        self.__render.append(r)

    def render_scene(self, screen):
        for i in self.__render:
            i.render(screen)

    def top(self, obj):
        self.__render.remove(obj)
        self.__render.append(obj)

    def __eq__(self, scene: str):
        return self.__scene == scene

'''class Transform:
    def __init__(self):
        self.anchor = 'topleft'
        self.__pos = 0
        self.__center_pos = 0

    @property
    def pos(self):
        if self.anchor == 'topleft':
            return self.__pos
        elif self.anchor == 'center':
            return self.__center_pos
        else:
            raise ValueError
    @pos.setter
    def pos(self, pos):
        if self.anchor == 'topleft':
            self.__pos = pos
        elif self.anchor == 'center':
            self.__center_pos = pos
        else:
            raise ValueError'''

class RectObject:
    def __init__(self, rect, color='magenta'):
        self.__rect = rect
        self.color = color
        Scene.active().add_render(self)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.__rect)

class GameObject(pygame.sprite.Sprite):
    def __init__(self, width=0, height=0, x=0, y=0, color='magenta'):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Scene.active().sprites.append(self)

class SpriteObject(GameObject):
    def __init__(self, image="sprites/placeholder.png", x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.anchor = 'center'
        Scene.active().add_render(self)

    @property
    def pos(self):
        if self.anchor == 'center': return self.rect.center
        elif self.anchor == 'topleft': return self.rect.topleft
        else: raise ValueError
    @pos.setter
    def pos(self, pos):
        if self.anchor == 'center': self.rect.center = pos
        elif self.anchor == 'topleft': self.rect.topleft = pos
        else: raise ValueError

    def render(self, screen):
        screen.blit(self.image, self.rect)

class Machine(SpriteObject):
    def __init__(self, image="sprites/placeholder.png"):
        super().__init__(image)
        Scene.active().draggable.append(self)

class Conveyor(SpriteObject):
    def __init__(self, pos):
        super().__init__("sprites/conveyor/conveyor1.png")
        self.pos = pos
        print('conveyor created')

class Grid:
    def __init__(self, size=(3,3)):
        super().__init__()
        self.size = list(size)
        self.__data = []
        for i in range(size[1]):
            self.__data.append(['None'] * size[0])
        self.grid_line_width = 6
        self.square_size = 80

        self.center_pos = (0,0)
        self.__calculate_bound()

        Scene.active().add_render(self)
        Scene.get('game').components['grid'] = self

    def __calculate_bound(self):
        self.bound_size = (self.square_size * self.size[0], self.square_size * self.size[1])
        self.__pos = (self.center_pos[0] - self.bound_size[0] // 2, self.center_pos[1] - self.bound_size[1] // 2)
        self.bound_pos = (self.__pos[0] + self.bound_size[0], self.__pos[1] + self.bound_size[1])

    def set_pos(self, pos):
        self.center_pos = pos
        self.__calculate_bound()

    def render(self, screen):
        # Draw background color
        pygame.draw.rect(screen, cf.grid_background,
                         pygame.Rect(self.__pos[0], self.__pos[1],
                                     self.square_size * self.size[0], self.square_size * self.size[1]))
        # Draw gridlines
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                tmp = pygame.Rect(self.__pos[0] + self.square_size * i, self.__pos[1] + self.square_size * j,
                                  self.square_size + self.grid_line_width, self.square_size + self.grid_line_width)
                                  # Makes grid lines same size
                pygame.draw.rect(screen, cf.grid_line, tmp, self.grid_line_width)

    def grow(self, side):
        if side == 0: self.size[0] += 1
        elif side == 1: self.size[1] += 1
        else: raise ValueError
        self.__calculate_bound()

    def in_grid(self, pos):
        return (self.__pos[0] < pos[0] < self.bound_pos[0] and
                self.__pos[1] < pos[1] < self.bound_pos[1])

    def get_square(self, pos):
        return (pos[0] - self.__pos[0]) // self.square_size, (pos[1] - self.__pos[1]) // self.square_size

    def snap_pos(self, pos):
        col, row = self.get_square(pos)
        return (self.__pos[0] + self.square_size*col + self.grid_line_width // 2 + self.square_size // 2,
                self.__pos[1] + self.square_size*row + self.grid_line_width // 2 + self.square_size // 2)

    def snap(self, ob, pos):
        if self.in_grid(pos):
            ob.pos = self.snap_pos(pos)

    def display_data(self):
        for i in self.__data:
            print(i)

    def empty_square(self, pos):
        col, row = self.get_square(pos)
        return self.__data[row][col] == 'None'

    def create(self, object):
        col, row = self.get_square(object.pos)
        if self.__data[row][col] == 'None':
            self.__data[row][col] = 'Full'
        self.display_data()
        #print(self.__data)