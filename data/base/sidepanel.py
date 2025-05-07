import pygame

from .object import RectObject, SpriteObject, TextObject
from data.config import WINDOW_SIZE, color_mid1, color_mid2, color_light1, color_dark2
from data import tools


class SidePanel:
    def __init__(self):
        self.components = {}
        s = self.components
        s['background'] = RectObject(pygame.Rect(0,0,300,WINDOW_SIZE[1]),color_mid1)

        s['topleft_panel'] = RectObject(pygame.Rect(35,40,110,110),color_mid2, radius=10, border_width=3)
        s['conveyor_image'] = SpriteObject(tools.GFX["conveyor"]["conveyor1"], 85, 90)
        s['conveyor_key_button'] = RectObject(pygame.Rect(85, 125, 70, 30), color_light1, radius=5, border_width=3,
                                              border_color=color_dark2)
        s['conveyor_key_text'] = TextObject("SPACE", 24, pos=(92, 133))

        s['topright_panel'] = RectObject(pygame.Rect(165, 40, 110, 110), color_mid2, radius=10)

        s['topleft_panel'].pos = (85, 90)
        s['topright_panel'].pos = (215, 90)

    def render(self, screen):
        for i in self.components.values():
            i.render(screen)