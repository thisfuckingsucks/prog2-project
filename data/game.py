import pygame, copy

from data.config import WINDOW_SIZE
from data.base import grid, sidepanel, selection, test, conveyor, timer, byte, ui, generator, instances
from data.base.machine import Machine


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

        self.grid.set_pos((800, WINDOW_SIZE[1] // 2))

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selection.place_direction = 90
                self.ui.update_direction()
            elif event.key == pygame.K_LEFT:
                self.selection.place_direction = 180
                self.ui.update_direction()
            elif event.key == pygame.K_DOWN:
                self.selection.place_direction = 270
                self.ui.update_direction()
            elif event.key == pygame.K_RIGHT:
                self.selection.place_direction = 0
                self.ui.update_direction()

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

        if self.mode == 'normal':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for obj in self.selection.draggable:
                        if obj.rect.collidepoint(event.pos):
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
        self.timer.count()

        self.objects.update_loop(self.grid)

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
                        self.grid.create(generator.Generator())