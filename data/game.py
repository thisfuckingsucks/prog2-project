import pygame, random, copy

from data.config import WINDOW_SIZE, grid_pos, SIZE
from data.base import grid, sidepanel, selection, test, conveyor, timer, byte, ui, generator, instances, info, machine


class Game:
    __timer = 0

    def __init__(self):
        self.mode = "normal"
        self.grid = grid.Grid()
        self.sidepanel = sidepanel.SidePanel()
        self.selection = selection.Selection()
        self.ui = ui.UI()
        self.timer = timer.Timer()
        self.objects = instances.ObjectInstances()
        self.info = info.Info()

        self.grid.set_pos((grid_pos, WINDOW_SIZE[1] // 2))

        self.test = test.Test()

        self.__top_render = []

    def render(self, screen):
        self.grid.render(screen)
        self.sidepanel.render(screen)
        self.test.render(screen)
        self.objects.render(screen)
        self.ui.render(screen)

    @classmethod
    def get_time(cls):
        return cls.__timer

    def event_loop(self, event):
        if not self.info.playing:
            if event.type == pygame.KEYDOWN:
                change = False
                if event.key == pygame.K_UP:
                    self.selection.place_direction = 90
                    change = True
                elif event.key == pygame.K_LEFT:
                    self.selection.place_direction = 180
                    change = True
                elif event.key == pygame.K_DOWN:
                    self.selection.place_direction = 270
                    change = True
                elif event.key == pygame.K_RIGHT:
                    self.selection.place_direction = 0
                    change = True
                if change:
                    self.ui.update_direction(self.selection.place_direction)
                    self.objects.update_direction(self.selection.place_direction, self.grid)

                if event.key == pygame.K_SPACE:
                    if self.mode != 'conveyor':
                        self.mode = 'conveyor'
                        self.sidepanel.components['topleft_panel'].outline_width = 4
                        self.sidepanel.components['topright_panel'].outline_width = 0
                    elif self.mode == 'conveyor':
                        self.mode = 'normal'
                        self.sidepanel.components['topleft_panel'].outline_width = 0

                if event.key == pygame.K_1:
                    if self.mode != 'generator':
                        self.mode = 'generator'
                        self.sidepanel.components['topright_panel'].outline_width = 4
                        self.sidepanel.components['topleft_panel'].outline_width = 0
                    elif self.mode == 'generator':
                        self.mode = 'normal'
                        self.sidepanel.components['topright_panel'].outline_width = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.info.choose:
                        bound = self.ui.play_button.get_bound()
                        if bound[0][0] < event.pos[0] < bound[0][1] and bound[1][0] < event.pos[1] < bound[1][1]:
                            self.start_round()
                    else: # choose state
                        for m in self.objects.machines:
                            if m.preview:
                                bound = m.get_bound()
                                if bound[0][0] < event.pos[0] < bound[0][1] and bound[1][0] < event.pos[1] < bound[1][1]:
                                    m.preview = False
                                    m.send_to_storage()
                                    for mach in self.objects.machines:
                                        if mach.preview:
                                            self.objects.machines.remove(mach)
                                            self.selection.draggable.remove(mach)
                                            mach.preview = False
                                            mach.pos = (WINDOW_SIZE[1]+100, 0)
                                    self.chosen()
                                    self.ui.render_choose = False
                                    self.info.choose = False

                if event.button == 3:
                    if self.grid.in_grid(event.pos):
                        obj = self.grid.object_at(event.pos)
                        if obj != 'None':
                            col, row = self.grid.get_index(obj)
                            self.grid.set_square(col, row, 'None')
                            if isinstance(obj, machine.Machine):
                                obj.send_to_storage()
                            elif isinstance(obj, conveyor.Conveyor):
                                self.objects.conveyors.remove(obj)
                            elif isinstance(obj, generator.Generator):
                                self.objects.generators.remove(obj)
                                self.selection.draggable.remove(obj)

            if self.mode == 'normal':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for obj in self.selection.draggable:
                            if obj.rect.collidepoint(event.pos):
                                if not obj.preview:
                                    # (object, dragging offset, original position)
                                    self.selection.current_dragging.append((obj,
                                                                            (event.pos[0] - obj.pos[0], event.pos[1] - obj.pos[1]),
                                                                            (obj.pos[0], obj.pos[1])))
                                    self.__top_render.append(obj)
                                    # Set grid square to none
                                    for row in self.grid.data:
                                        if obj in row:
                                            i = row.index(obj)
                                            row[i] = 'None'
                                            break
                if event.type == pygame.MOUSEMOTION:
                    if self.selection.current_dragging:
                        for obj in self.selection.current_dragging:
                            obj[0].pos = (event.pos[0] - obj[1][0], event.pos[1] - obj[1][1])
                            if self.grid.in_grid(event.pos):
                                if self.grid.empty_square(event.pos):
                                    self.grid.obj_snap(obj[0], event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for obj_pair in self.selection.current_dragging:
                            if self.grid.in_grid(event.pos):
                                col, row = self.grid.get_square(event.pos)
                                if self.grid.empty_square(event.pos):
                                    self.grid.obj_snap(obj_pair[0], event.pos)
                                    self.grid.set_square(col, row, obj_pair[0])
                                else: ...
                            else: ...
                        self.selection.current_dragging.clear()

            elif self.mode == 'conveyor':
                self.conveyor_mode(event)

            elif self.mode == 'generator':
                self.generator_mode(event)

    def update_loop(self):
        self.timer.animation_count()

        if self.info.playing:
            self.objects.update_loop(self.grid, self.info, self.timer)

        if self.info.playing:
            self.timer.count()
            if self.timer.clock <= 0:
                self.end_round()

        self.ui.update_loop(self.info, self.timer)

        self.sidepanel.update_loop(self.objects.machines)

    def start_round(self):
        if self.info.state is None:
            self.info.start_round()
            self.timer.start_round(self.info)
            self.ui.start_round(self.info)

    def end_round(self):
        self.info.end_round()
        if self.info.state is None:
            self.objects.end_round()
            self.grid.end_round(self.info)
            self.ui.end_round(self.info)

            mach1 = machine.Machine()
            mach1.pos = (WINDOW_SIZE[0]//2 - 200, 520)
            mach1.preview = True
            del mach1
            mach2 = machine.Machine()
            mach2.pos = (WINDOW_SIZE[0] // 2, 520)
            mach2.preview = True
            del mach2
            mach3 = machine.Machine()
            mach3.pos = (WINDOW_SIZE[0] // 2 + 200, 520)
            mach3.preview = True
            del mach3

    def chosen(self):
        self.ui.render_choose = False
        self.info.choose = False
        for mach in self.objects.machines:
            if mach.preview:
                self.objects.machines.remove(mach)
                self.selection.draggable.remove(mach)
                mach.preview = False
                mach.pos = (WINDOW_SIZE[1] + 100, 0)

    def conveyor_mode(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.grid.in_grid(event.pos):
                    if self.grid.empty_square(event.pos):
                        self.grid.create(conveyor.Conveyor(self.grid.snap_pos(event.pos), self.selection.get_direction()))
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass

    def generator_mode(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.grid.in_grid(event.pos):
                    if self.grid.empty_square(event.pos):
                        gen = generator.Generator()
                        gen.pos = self.grid.snap_pos(event.pos)
                        self.grid.create(gen)
                        gen.set_direction(self.selection.place_direction)