import pygame as pygame
from config import Config as cf
from sys import exit
from game_classes import *
from game_func import *

from game_display import Display

pygame.init()
screen = pygame.display.set_mode((cf.window_width, cf.window_height))
pygame.display.set_caption('game')
clock = pygame.time.Clock()

test_font = pygame.font.SysFont('Bahnschrift', 50,False)
test_font2 = pygame.font.SysFont('Consolas', 50,False)

thing = pygame.Surface((50,50))
thing.fill('Red')
text_surface = test_font.render('abswobboswuoswhso', False,cf.text_color)
text_surface2 = test_font2.render('TEST', False,'white')

box = pygame.Rect(200,300,200,300)
drag = False

#grid = Grid()
machine = Machine(1)
machine.xy = [400,400]
grid = Grid()
grid.z = -10
grid.center((cf.window_width//2 + 200, cf.window_height//2))
grid.grow(0)
grid.grow(1)
panel = GameObject(pygame.Surface((300,cf.window_height)),color=cf.panel_color1)

sprites = pygame.sprite.Group()

while True:
    screen.fill(cf.background_color)

    check_input()

    grid.snap(machine)

    GameInfo.display.render(screen)

    screen.blit(text_surface,(200,200))

    #debug

    pygame.display.update()
    clock.tick(cf.fps)