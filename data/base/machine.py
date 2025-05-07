
from data.base.object import SpriteObject
from data.base.conveyor import Conveyor
from data.base.byte import Byte
from data.base.timer import Timer
from data.base.selection import Selection
from data import tools


class Machine(SpriteObject):
    __instances = []

    @staticmethod
    def instances():
        return Machine.__instances

    def __init__(self, image=tools.GFX["other"]["placeholder"]):
        super().__init__(image)
        #Scene.active().draggable.append(self)
        self.input = (1, -1, 0)
        self.output = (1, 1, 0)

        Machine.__instances.append(self)
        Selection.get().draggable.append(self)

    def __repr__(self):
        return '<Mach>'

    def update_loop(self, grid):
        # grid = Grid.instance()
        if grid.part_of_grid(self):
            # i, j = row, col
            [i, j] = grid.get_index(self)
            if i > 0: ...
            if j > 0: ...
            if i < len(grid.data[0]) - 1:
                if self.output[1] == 1:
                    if isinstance(grid.data[i + 1][j], Conveyor):
                        if Timer.get_time() == 0:
                            byt = Byte()
                            byt.pos = self.pos
                            axis = self.output[0]
                            x = self.output[1]
                            direction = [0, 0]
                            direction[axis] = x
                            byt.direction = direction
            if j < len(grid.data) - 1: ...