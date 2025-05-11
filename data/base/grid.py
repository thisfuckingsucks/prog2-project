from data.config import SIZE, color_light1, color_mid3, goal_green, goal_width
import pygame


class Grid:
    __instance = None

    @staticmethod
    def instance():
        return Grid.__instance

    def __init__(self, size=(3,3)):
        super().__init__()
        Grid.__instance = self

        self.size = list(size)
        self.__data = []
        for i in range(size[1]):
            self.__data.append(['None'] * size[0])
        self.grid_line_width = 6
        self.square_size = SIZE

        self.center_pos = (0,0)
        self.__calculate_bound()

    @property
    def data(self):
        return self.__data

    def part_of_grid(self, obj):
        for row in self.data:
            if obj in row:
                return True
        return False

    def get_index(self, obj):
        for i, row in enumerate(self.data):
            for j, square in enumerate(row):
                if obj is square:
                    return j, i
        raise ValueError("object not found in grid") # col, row

    def check_square(self, obj, obj_class, check):
        # (0,1)
        col, row = self.get_index(obj)
        target = (col + check[0], row + check[1])
        if (target[0] < 0 or target[0] >= self.size[0] or
            target[1] < 0 or target[1] >= self.size[1]):
            return False
        return isinstance(self.__data[target[1]][target[0]], obj_class)

    def __calculate_bound(self):
        self.bound_size = (self.square_size * self.size[0], self.square_size * self.size[1])
        self.__pos = (self.center_pos[0] - self.bound_size[0] // 2, self.center_pos[1] - self.bound_size[1] // 2)
        self.bound_pos = (self.__pos[0] + self.bound_size[0], self.__pos[1] + self.bound_size[1])

    def set_pos(self, pos):
        self.center_pos = pos
        self.__calculate_bound()
        """self.goal.update(self.bound_pos[0] + self.grid_line_width, self.__pos[1],
                         goal_width, SIZE*self.size[1] + self.grid_line_width)"""

    def render(self, screen):
        # Draw background color
        pygame.draw.rect(screen, color_light1,
                         pygame.Rect(self.__pos[0], self.__pos[1],
                                     self.square_size * self.size[0], self.square_size * self.size[1]))
        # Draw gridlines
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                tmp = pygame.Rect(self.__pos[0] + self.square_size * i, self.__pos[1] + self.square_size * j,
                                  self.square_size + self.grid_line_width, self.square_size + self.grid_line_width)
                                  # Makes grid lines same size
                pygame.draw.rect(screen, color_mid3, tmp, self.grid_line_width)

        pygame.draw.rect(screen, goal_green, pygame.Rect(self.bound_pos[0] + self.grid_line_width, self.__pos[1],
                                                         goal_width, SIZE*self.size[1] + self.grid_line_width))

    def grow(self, side):
        if side == 0:
            self.size[0] += 1
            for row in self.__data:
                row += ['None']
        elif side == 1:
            self.size[1] += 1
            self.__data.append(['None'] * self.size[0])
        else:
            raise ValueError
        self.__calculate_bound()
        for row in self.__data:
            for obj in row:
                if obj != 'None':
                    obj.pos = self.snap_pos((obj.pos[0]-10, obj.pos[1]-10))

    def end_round(self, info):
        self.grow(info.next_grow)

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

    def create(self, obj):
        #from data.base import machine

        col, row = self.get_square(obj.pos)
        if self.__data[row][col] == 'None':
            #if isinstance(obj, machine.Machine):
            #Scene.active().info.machines.append((object, row, col))
            self.__data[row][col] = obj
        self.display_data()
        #print(self.__data)

    def object_at(self, pos):
        col, row = self.get_square(pos)
        return self.__data[row][col]