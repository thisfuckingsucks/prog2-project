from game_classes2 import *


class Generator(RectObject):
    def __init__(self):
        rect = pygame.Rect(0, 0, cf.SIZE, cf.SIZE)
        color = cf.generator1
        radius = 10
        super().__init__(rect, color, radius)
        self.border_color = cf.dark_color1

    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, self.border_color, self._rect, width=4, border_radius=self.radius)