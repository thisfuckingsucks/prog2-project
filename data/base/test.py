from data.base.machine import Machine
from data.base.generator import Generator


class Test:
    def __init__(self):
        self.components = {}
        s = self.components

    def render(self, screen):
        for i in self.components.values():
            i.render(screen)