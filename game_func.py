from game_classes import *
from sys import exit


def check_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for o in GameInfo.draggable:
                    if o.rect.collidepoint(event.pos):
                        GameInfo.dragging.append(o)
                        GameInfo.drag_xy.append((event.pos[0]-o.x, event.pos[1]-o.y))
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                GameInfo.dragging.clear()
                GameInfo.drag_xy.clear()
        if event.type == pygame.MOUSEMOTION:
            if GameInfo.dragging:
                for i,o in enumerate(GameInfo.dragging):
                    o.x = event.pos[0] - GameInfo.drag_xy[i][0]
                    o.y = event.pos[1] - GameInfo.drag_xy[i][1]





