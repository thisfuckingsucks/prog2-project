from data.config import fps


class Timer:
    __timer = 0

    @staticmethod
    def get_time():
        return Timer.__timer

    @staticmethod
    def count():
        Timer.__timer += 1
        if Timer.__timer >= fps*10:
            Timer.__timer = 0