import typing


class Effect:
    name: str
    action_func: typing.Callable[[object], None]
    duration: int
    delay: float
    finished: bool
    __counter: int

    def __init__(self,
                 name: str,
                 action_func: typing.Callable[[object], None],
                 duration: int,
                 delay: float):
        self.name = name
        self.action_func = action_func
        self.duration = duration
        self.delay = delay
        self.__counter = 0
        self.finished = True

    def start(self):
        self.finished = False
        self.__counter = 0

    def update(self, entity: object):
        if self.finished:
            return
        self.action_func(entity)
        self.__counter += 1
        if self.__counter >= self.duration:
            self.finished = True

