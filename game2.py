import pygame
from config import Config as cf
from sys import exit
from game_classes2 import *
from game_classes21 import *
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
RectObject(pygame.Rect(35,40,100,100),cf.panel_color2, radius=10)
RectObject(pygame.Rect(165,40,100,100),cf.panel_color2, radius=10)
machine = Machine()
machine.pos = (200,200)
conveyor = Conveyor((600,400))
grid.display_data()
byte = Byte()

while True:
    screen.fill(cf.background_color)

    app_loop()

    game_scene.render_scene(screen)

    pygame.display.update()
    clock.tick(cf.fps)