import pygame

from data.base.object import RectObject, SpriteObject, TextObject
from data.config import WINDOW_SIZE
from data import tools
from data.base.selection import Selection


class UI:
    def __init__(self):
        self.components = {}
        s = self.components
        s['direction'] = SpriteObject(tools.GFX["other"]['direction-arrow'],WINDOW_SIZE[0]-100,WINDOW_SIZE[1]-100)
        s['direction'].angle = 0

        self.update_direction()

    def update_direction(self):
        self.components["direction"].set_direction(Selection.get().place_direction)

    def render(self, screen):
        for i in self.components.values():
            i.render(screen)