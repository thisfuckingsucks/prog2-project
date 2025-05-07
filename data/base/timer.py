


class Timer:
    __timer = 0

    @staticmethod
    def get_time():
        return Timer.__timer

    @staticmethod
    def count():
        Timer.__timer += 1
        if Timer.__timer >= 60:
            Timer.__timer = 0