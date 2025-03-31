from game_classes2 import *
from sys import exit


global scene
global grid

def app_loop(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    global scene
    scene = Scene.active()
    if scene == 'game':
        game_loop(event)

def game_loop(event):
    global grid
    grid = scene.components['grid']

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
        if event.type == pygame.MOUSEMOTION:
            if scene.dragging:
                for o in scene.dragging:
                    o[0].pos = (event.pos[0] - o[1][0], event.pos[1] - o[1][1])
                    if grid.in_grid(event.pos):
                        if grid.empty_square(event.pos):
                            grid.snap(o[0], event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                scene.dragging.clear()

    elif scene.mode == 'conveyor':
        conveyor_mode(event)

'''def game_input(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for o in Scene.active().draggable:
                if o.rect.collidepoint(event.pos):
                    Scene.active().dragging.append((o, (event.pos[0]-o.pos[0], event.pos[1]-o.pos[1])))
                    # GameInfo.dragging.append(o)
                    # GameInfo.drag_xy.append((event.pos[0]-o.x, event.pos[1]-o.y))
    if event.type == pygame.MOUSEMOTION:
        if Scene.active().dragging:
            for o in Scene.active().dragging:
                o[0].pos = (event.pos[0] - o[1][0], event.pos[1] - o[1][1])
                #o.x = event.pos[0] - GameInfo.drag_xy[i][0]
                #o.y = event.pos[1] - GameInfo.drag_xy[i][1]
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            Scene.active().dragging.clear()
            # GameInfo.dragging.clear()
            # GameInfo.drag_xy.clear()
    if event.type == pygame.K_SPACE:
        Scene.active()
    if event.type == pygame.K_SPACE:
        Scene.active().conveyor = not Scene.active().conveyor'''

def conveyor_mode(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if grid.in_grid(event.pos):
                if grid.empty_square(event.pos):
                    grid.create(Conveyor(grid.snap_pos(event.pos)))