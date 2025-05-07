import pygame
import sys

from data.config import WINDOW_SIZE, fps, color_light0


pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
pygame.display.set_caption('game')
clock = pygame.time.Clock()


from data.game import Game


class App:
    def __init__(self):
        self.scene = "game"
        self.game = Game()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.game.event_loop(event)

    def update_loop(self):
        self.game.update_loop()

    def run(self):
        while True:
            screen.fill(color_light0)

            #app_loop()
            self.event_loop()
            self.update_loop()

            self.game.render(screen)

            pygame.display.update()
            clock.tick(fps)

App().run()