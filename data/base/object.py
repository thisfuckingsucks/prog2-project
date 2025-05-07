import pygame
from data import tools
from data.base import timer


class TextObject:
    def __init__(self, text="placeholder", size=32, color=(0,0,0), pos=(0,0)):
        self.font = pygame.font.Font(None, size)
        self.color = color
        self.text = text
        self.pos = pos
        #Scene.active().add_render(self)

    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, text):
        self._text = text
        self._surface = self.font.render(self.text, False, self.color)

    def render(self, screen):
        screen.blit(self._surface,self.pos)

class RectObject:
    def __init__(self, rect, color='magenta', radius=0, border_width=0, border_color=(255,255,255),
                 outline_width=0, outline_color=(0,0,0)):
        self._rect = rect
        self.color = color
        self.radius = radius
        self.border_width = border_width
        self.border_color = border_color
        self._outline = rect.copy()
        self._outline.inflate(outline_width * 2, outline_width * 2)
        self._outline_width = outline_width
        self.outline_color = outline_color
        self.__pos = (0, 0)
        #Scene.active().add_render(self)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self._rect, border_radius=self.radius)
        if self.border_width != 0:
            pygame.draw.rect(screen, self.border_color, self._rect, border_radius=self.radius, width=self.border_width)
        if self._outline_width != 0:
            pygame.draw.rect(screen, self.outline_color, self._outline, border_radius=self.radius, width=self._outline_width)

    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self, pos):
        self.__pos = pos
        self._rect.center = (int(pos[0]), int(pos[1]))
        self._outline.center = (int(pos[0]), int(pos[1]))

    @property
    def outline_width(self):
        return self._outline_width
    @outline_width.setter
    def outline_width(self, width):
        self._outline = self._rect.copy()
        self._outline.inflate_ip(width * 2, width * 2)
        self._outline_width = width

class GameObject(pygame.sprite.Sprite):
    def __init__(self, width=0, height=0, x=0, y=0, color='magenta'):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Scene.active().sprites.append(self)

class SpriteObject(GameObject):
    def __init__(self, image=tools.GFX["other"]["placeholder"], x=0, y=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.anchor = 'center'
        self.angle = 270

    @property
    def pos(self):
        if self.anchor == 'center': return self.rect.center
        elif self.anchor == 'topleft': return self.rect.topleft
        else: raise ValueError
    @pos.setter
    def pos(self, pos):
        if self.anchor == 'center': self.rect.center = pos
        elif self.anchor == 'topleft': self.rect.topleft = pos
        else: raise ValueError

    def set_direction(self, angle):
        rotation = angle - self.angle
        self.image = pygame.transform.rotate(self.image, rotation)
        self.angle = angle

    def render(self, screen):
        screen.blit(self.image, self.rect)

class AnimatedSpriteObject(SpriteObject):
    def __init__(self, sprites):
        super().__init__(sprites[0])
        self.sprites = list(sprites)
        self.current = 0
        self.speed = 1
        self.__counter = 0

    def set_direction(self, angle):
        rotation = angle - self.angle
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.rotate(self.sprites[i], rotation)
        self.angle = angle

    def update(self):
        """self.__counter += 1
        if self.__counter >= self.speed:
            self.__counter = 0

            self.current += 1
            if self.current >= len(self.sprites):
                self.current = 0"""
        self.current = timer.Timer.get_time() % 10
        self.image = self.sprites[self.current]

    def render(self, screen):
        self.update()
        super().render(screen)