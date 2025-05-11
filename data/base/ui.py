import pygame

from data.base.object import RectObject, SpriteObject, TextObject
from data.config import (WINDOW_SIZE, progress_bar_size, color_dark2, color_dark3, progress_bar_pos, goal_green, WHITE,
byte_goal_red, byte_current_blue)
from data import tools


class UI:
    def __init__(self):
        self.components = {}
        s = self.components
        s['direction'] = SpriteObject(tools.GFX["other"]['direction-arrow'],WINDOW_SIZE[0]-100,WINDOW_SIZE[1]-100)
        s['direction'].angle = 0

        self.update_direction(270)

        rect = pygame.Rect(0, 0, progress_bar_size[0], progress_bar_size[1])
        s['progress_bar_back'] = RectObject(rect, color_dark2, outline_color=color_dark3, outline_width=5)
        s['progress_bar_back'].pos = progress_bar_pos
        rect = pygame.Rect(0, 0, progress_bar_size[0], progress_bar_size[1])
        s['progress_bar_current'] = RectObject(rect, goal_green)
        s['progress_bar_current'].pos = progress_bar_pos
        s['round_goal'] = TextObject("100", 48, byte_goal_red, center=(0, progress_bar_pos[1]))
        s['round_current'] = TextObject("0", 48, byte_current_blue, center=(0, progress_bar_pos[1]))

        self.play_button = SpriteObject(tools.GFX['other']['start-button'])
        self.play_button.pos = (380,80)
        s['clock'] = SpriteObject(tools.GFX['other']['clock'])
        s['clock'].pos = (WINDOW_SIZE[0]-70, 70)
        s['clock_time'] = TextObject("10", 48, (0,0,0), pos=(WINDOW_SIZE[0]-85, 62), centered=False)
        s['level_text'] = TextObject("Level 0", 56, (0,0,0), pos=(300+20,WINDOW_SIZE[1]-50), centered=False)

        self.__render_play = True

        #self.victory_text = TextObject("VICTORY", 138,)

        self.back_panel = pygame.Surface((800, 200), flags=pygame.SRCALPHA)
        self.back_panel.fill(pygame.Color(0,0,0,80))
        self.back_rect = self.back_panel.get_rect()
        self.back_rect.center = (WINDOW_SIZE[0]//2, 500)
        self.choose_text = TextObject("CHOOSE", 72, WHITE, pos=(530, 420), centered=False)
        self.render_choose = False

    def update_direction(self, angle):
        self.components["direction"].set_direction(angle)

    def render(self, screen):
        for i in self.components.values():
            i.render(screen)

        if self.__render_play:
            self.play_button.render(screen)

        if self.render_choose:
            screen.blit(self.back_panel, self.back_rect)
            self.choose_text.render(screen)

    def update_loop(self, info, timer):
        s = self.components
        s['round_current'].text = info.round_progress
        s['round_goal'].text = info.round_goal

        rect = s['progress_bar_current'].rect
        s['progress_bar_current'].rect.update(rect.left , rect.top,
                                              int(progress_bar_size[0] * (info.round_progress / info.round_goal)),
                                              progress_bar_size[1])

        s['round_goal'].rect.midleft = (progress_bar_pos[0] + progress_bar_size[0]//2 + 20, progress_bar_pos[1])
        s['round_current'].rect.midright = (progress_bar_pos[0] - progress_bar_size[0] // 2 - 20, progress_bar_pos[1])

        s['clock_time'].text = timer.clock

    def start_round(self, info):
        self.__render_play = False

    def end_round(self, info):
        self.__render_play = True
        self.components['level_text'].text = f"Level {info.level}"
        self.render_choose = True