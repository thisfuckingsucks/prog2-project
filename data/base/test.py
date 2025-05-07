from data.base.machine import Machine


class Test:
    def __init__(self):
        self.components = {}
        s = self.components

        s['machine'] = Machine()
        s['machine'].pos = (200, 200)

    def render(self, screen):
        for i in self.components.values():
            i.render(screen)