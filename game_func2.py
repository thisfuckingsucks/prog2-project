import pygame

from game_classes2 import *
from sys import exit



global scene
global grid
global selection
global info

def app_loop():
    global scene
    global info
    scene = Scene.active()
    info = scene.info

    scene.counter += 1
    if scene.counter >= 60:
        scene.counter = 0

    for event in pygame.event.get():
        app_input(event)

    if scene == 'game':
        global grid
        grid = scene.components['grid']
        game_loop()

def app_input(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    if scene == 'game':
        game_input(event)

def game_loop():
    for byte in info.bytes:
        '''if grid.in_grid(byte.pos):
            col, row = grid.get_square(byte.pos)
            if isinstance(info.grid[row][col], Machine):
                mach = info.grid[row][col]
                axis = mach.output[0]
                byte.pos = (byte.pos[0] + cf.SIZE/cf.fps,
                            byte.pos[1] - cf.SIZE/cf.fps)'''
        if grid.in_grid(byte.pos):
            byte.pos = (byte.pos[0] + (cf.SIZE / cf.fps * byte.direction[0]),
                        byte.pos[1] + (cf.SIZE / cf.fps * byte.direction[1]))

            center = grid.snap_pos(byte.pos)
            if center[0] - 1 <= byte.pos[0] <= center[0] + 1 and center[1] - 1 <= byte.pos[1] <= center[1] + 1:
                col, row = grid.get_square(byte.pos)
                obj = info.grid[row][col]
                if obj == 'None':
                    byte.direction = (0,0)
                elif isinstance(obj, Conveyor):
                    conv = obj
                    byte.direction = conv.direction

    # i, j = row, col
    for mach, i, j in info.machines:
        if i > 0: ...
        if j > 0: ...
        if i < len(info.grid[0]) - 1:
            if mach.output[1] == 1:
                if isinstance(info.grid[i+1][j], Conveyor):
                    if scene.counter == 0:
                        byte = Byte()
                        byte.pos = mach.pos
                        '''if mach.output[0] == 1: axis = 1
                        elif mach.output[0] == 0: axis = 0
                        else: axis = None'''
                        axis = mach.output[0]
                        '''if mach.output[1] == 1: x = 1
                        elif mach.output[1] == -1: x = -1
                        else: x = None'''
                        x = mach.output[1]
                        direction = [0,0]
                        direction[axis] = x
                        byte.direction = direction
        if j < len(info.grid) - 1: ...

    for i, row in enumerate(info.grid):
        for j, obj in enumerate(row):
            pass

def game_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if scene.mode == 'normal':
                scene.mode = 'conveyor'
            elif scene.mode == 'conveyor':
                scene.mode = 'normal'

    if scene.mode == 'normal':
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for o in scene.draggable:
                    if o.rect.collidepoint(event.pos):
                        scene.dragging.append((o, (event.pos[0]-o.pos[0], event.pos[1]-o.pos[1])))
                        scene.top(o)
                        if isinstance(o, Machine):
                            machine_only = [x[0] for x in info.machines]
                            if o in machine_only:
                                i = machine_only.index(o)
                                info.machines.pop(i)
                        for row in info.grid:
                            if o in row:
                                i = row.index(o)
                                row[i] = 'None'
                                break
        if event.type == pygame.MOUSEMOTION:
            if scene.dragging:
                for o in scene.dragging:
                    o[0].pos = (event.pos[0] - o[1][0], event.pos[1] - o[1][1])
                    if grid.in_grid(event.pos):
                        if grid.empty_square(event.pos):
                            grid.obj_snap(o[0], event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for obj_pair in scene.dragging:
                    if grid.in_grid(event.pos):
                        col, row = grid.get_square(event.pos)
                        if grid.empty_square(event.pos):
                            grid.obj_snap(obj_pair[0], event.pos)
                            grid.set_square(col, row, obj_pair[0])
                        if isinstance(obj_pair[0], Machine):
                            info.machines.append((obj_pair[0], row, col))
                scene.dragging.clear()

    elif scene.mode == 'conveyor':
        conveyor_mode(event)

#def game_input(event):


def conveyor_mode(event):
    global info
    info = Scene.active().info
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP: info.place_direction = (0,-1)
        elif event.key == pygame.K_LEFT: info.place_direction = (-1,0)
        elif event.key == pygame.K_DOWN: info.place_direction = (0,1)
        elif event.key == pygame.K_RIGHT: info.place_direction = (1,0)
        print('right')
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            #selection.down = 1
            if grid.in_grid(event.pos):
                #selection.current = grid.get_square(event.pos)
                if grid.empty_square(event.pos):
                    grid.create(Conveyor(grid.snap_pos(event.pos), info.place_direction))
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            pass
            #selection.up()