import pygame
from config import Config as cf
from game_tool_func import *


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
        self.dragging = [] # (object, (pos))
        self.mode = 'None'
        self.components = {}
        self.counter = 0
        self.info = Info()
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

class Selection:
    def __init__(self):
        Scene.active().components['selection'] = self
        self.previous = 0
        self.__current = 0
        self.preview = 0
        self.down = 0

    @property
    def current(self):
        return self.__current
    @current.setter
    def current(self, x):
        self.previous = self.__current
        self.__current = x

    def up(self):
        self.previous = 0
        self.__current = 0

class Info:
    def __init__(self):
        self.place_direction = (0,1)
        self.grid = []
        self.machines = [] # (Machine, row, col)
        self.bytes = [] # Byte

class RectObject:
    def __init__(self, rect, color='magenta', radius=0):
        self._rect = rect
        self.color = color
        self.radius = radius
        Scene.active().add_render(self)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self._rect, border_radius=self.radius)

class Byte(RectObject):
    def __init__(self):
        rect = pygame.Rect(0, 0, 50, 50)
        super().__init__(rect, cf.dark_color1)
        self.direction = (0,0)
        self.__pos = [0,0]
        Scene.active().info.bytes.append(self)

    def render(self, screen):
        pygame.draw.rect(screen, cf.grid_background, self._rect, border_radius=10)
        pygame.draw.rect(screen, self.color, self._rect, width=4, border_radius=10)

    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self, pos):
        self.__pos = pos
        self._rect.center = (int(pos[0]), int(pos[1]))

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

class AnimatedSpriteObject(SpriteObject):
    def __init__(self, sprites):
        super().__init__(sprites[0])
        self.sprites = load_images(sprites)
        self.current = 0
        self.speed = 1
        self.__counter = 0

    def update(self):
        self.__counter += 1
        if self.__counter >= self.speed:
            self.__counter = 0

            self.current += 1
            if self.current >= len(self.sprites):
                self.current = 0
            self.current = Scene.active().counter % 10
            self.image = self.sprites[self.current]

    def render(self, screen):
        self.update()
        super().render(screen)

class Machine(SpriteObject):
    def __init__(self, image="sprites/placeholder.png"):
        super().__init__(image)
        Scene.active().draggable.append(self)
        self.input = (1, -1, 0)
        self.output = (1, 1, 0)

    def __repr__(self):
        return '<Mach>'

class Conveyor(AnimatedSpriteObject):
    def __init__(self, pos, dir=(0,-1)):
        super().__init__(cf.conveyor_sprites)
        self.pos = pos
        self.speed = 1
        print('conveyor created')
        self.direction = (0,0)
        self.__update_direction(dir)

    def __repr__(self):
        return 'Convey'

    def __update_direction(self, x):
        if x == (1,0): angle = 90
        elif x == (0,-1): angle = 180
        elif x == (-1,0): angle = 270
        else: angle = 0
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.rotate(self.sprites[i], angle)
        self.direction = x
        print(angle)

    '''def set_direction(self, dir):
        if dir == 'down': x = 0
        elif dir == 'right': x = 1
        elif dir == 'up': x = 2
        elif dir == 'left': x = 3
        self.__update_direction(x)

    def rotate(self):
        x = self.direction + 1
        if x > 3: x = 0
        self.__update_direction(x)'''

class Grid:
    def __init__(self, size=(3,3)):
        super().__init__()
        self.size = list(size)
        self.__data = Scene.active().info.grid
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
        return int((pos[0] - self.__pos[0]) // self.square_size), int((pos[1] - self.__pos[1]) // self.square_size)
    # col, row

    def snap_pos(self, pos):
        col, row = self.get_square(pos)
        return (self.__pos[0] + self.square_size*col + self.grid_line_width // 2 + self.square_size // 2,
                self.__pos[1] + self.square_size*row + self.grid_line_width // 2 + self.square_size // 2)

    def snap(self, ob, pos):
        if self.in_grid(pos):
            ob.pos = self.snap_pos(pos)

    def obj_snap(self, obj, pos):
        if self.in_grid(pos):
            col, row = self.get_square(pos)
            obj.pos = (self.__pos[0] + self.square_size*col + self.grid_line_width // 2 + self.square_size // 2,
                       self.__pos[1] + self.square_size*row + self.grid_line_width // 2 + self.square_size // 2)

    def set_square(self, col, row, obj):
        self.__data[row][col] = obj

    def display_data(self):
        for i in self.__data:
            print(i)

    def empty_square(self, pos):
        col, row = self.get_square(pos)
        return self.__data[row][col] == 'None'

    def create(self, object):
        col, row = self.get_square(object.pos)
        if self.__data[row][col] == 'None':
            if isinstance(object, Machine):
                Scene.active().info.machines.append((object, row, col))
            self.__data[row][col] = object
        self.display_data()
        #print(self.__data)