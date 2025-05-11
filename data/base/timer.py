from data.config import fps


class Timer:
    __animation_timer = 0

    @staticmethod
    def get_animation_time():
        return Timer.__animation_timer

    @staticmethod
    def animation_count():
        Timer.__animation_timer += 1
        if Timer.__animation_timer >= fps*10:
            Timer.__animation_timer = 0

    def __init__(self):
        self.clock = 10
        self.timer = 0

    def count(self):
        self.timer += 1
        if self.timer%fps == 0:
            self.clock -= 1
        if self.timer >= fps*10:
            self.timer = 0

    def start_round(self, info):
        self.clock = info.round_limit
        self.timer = 0