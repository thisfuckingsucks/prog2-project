
from data.config import level_scaling


class Info:
    def __init__(self):
        self.playing = False
        self.level = 0
        self.round_goal = 10
        self.round_limit = 10
        self.round_progress = 0
        self.next_grow = 0
        self.state = None
        self.choose = False

    def end_round(self):
        if self.round_progress >= self.round_goal:
            self.level_up()
            self.round_progress = 0
        else:
            self.state = 'LOSE'
        if self.next_grow == 0:
            self.next_grow = 1
        elif self.next_grow == 1:
            self.next_grow = 0
        self.playing = False

    def level_up(self):
        self.level += 1
        self.round_goal = int(self.round_goal * level_scaling)
        self.round_limit += 2
        self.choose = True

    def start_round(self):
        self.playing = True