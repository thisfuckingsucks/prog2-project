import pygame
from config import Config as cf
from sys import exit
from game_classes2 import *
from game_func2 import *


# Setup
pygame.init()
screen = pygame.display.set_mode((cf.window_width, cf.window_height))
pygame.display.set_caption('game')
clock = pygame.time.Clock()

# Game
game_scene = Scene("game")
game_scene.mode = 'normal'
Scene.set_to(game_scene)
grid = Grid()
grid.set_pos((800, cf.window_height//2))

panel = RectObject(pygame.Rect(0,0,300,cf.window_height),cf.panel_color1)
machine = Machine()
machine.pos = (200,200)
conveyor = Conveyor((600,400))
grid.display_data()

while True:
    screen.fill(cf.background_color)

    for event in pygame.event.get():
        app_loop(event)

    game_scene.render_scene(screen)

    pygame.display.update()
    clock.tick(cf.fps)