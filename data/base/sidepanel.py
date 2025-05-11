import pygame

from data.base.object import RectObject, SpriteObject, TextObject
from data.base.generator import Generator
from data.config import WINDOW_SIZE, color_mid1, color_mid2, color_light1, color_dark2, WHITE, SIZE, selection_outline_width
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
        s['conveyor_key_text'] = TextObject("SPACE", 24, pos=(92, 133), centered=False)

        s['topright_panel'] = RectObject(pygame.Rect(165, 40, 110, 110), color_mid2, radius=10, border_width=3)
        s['generator_image'] = SpriteObject(tools.GFX["generator"]["generator1"], 215, 90)
        s['generator_key_button'] = RectObject(pygame.Rect(255, 125, 30, 30), color_light1, radius=5, border_width=3,
                                              border_color=color_dark2)
        s['generator_key_text'] = TextObject("1", 28, pos=(265, 130), centered=False)
        s['generator_key_number'] = TextObject("+1", 48, center=(215, 90), color=WHITE)

        s['topleft_panel'].pos = (85, 90)
        s['topright_panel'].pos = (215, 90)

        s['machine_storage'] = RectObject(pygame.Rect(0,0,300-SIZE//2,WINDOW_SIZE[1]-320), color_mid2, radius=10)

        #(random.randint(SIZE, 300 - SIZE), random.randint(150 + SIZE, WINDOW_SIZE[1] - SIZE))
        s['machine_storage'].pos = (300//2, 500)

        self.selected_machine = None
        self.selected_rect = None
        self.machine_panel = {}
        m = self.machine_panel
        m['back_panel'] = RectObject(pygame.Rect(0,0,300-SIZE//2,110), color_light1, radius=10, border_width=5,
                                     border_color=color_dark2)
        m['back_panel'].pos = (300//2, 230)
        m['function_text'] = TextObject("Function: ", 42, color_dark2, pos=(40, 200), centered=False)
        m['cooldown_text'] = TextObject("Cooldown: ", 32, color_dark2, pos=(40, 240), centered=False)

    def render(self, screen):
        for i in self.components.values():
            i.render(screen)

        if self.selected_machine is not None:
            for i in self.machine_panel.values():
                i.render(screen)
            pygame.draw.rect(screen, WHITE, self.selected_rect, selection_outline_width)

    def update_loop(self, machines):
        self.selected_machine = None
        self.selected_rect = None
        mouse = pygame.mouse.get_pos()
        for m in machines:
            bound = m.get_bound()
            if bound[0][0] < mouse[0] < bound[0][1] and bound[1][0] < mouse[1] < bound[1][1]:
                self.selected_machine = m
                self.selected_rect = m.rect.inflate(selection_outline_width,selection_outline_width)
                self.machine_panel['function_text'].text = f"Function: {m.function_text}"
                self.machine_panel['cooldown_text'].text = f"Cooldown: {m.sec_cooldown} secs"