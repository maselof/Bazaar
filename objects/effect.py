import typing


class Effect:
    name: str
    action_func: typing.Callable[[object, float], None]
    duration: int
    delay: float
    value: float
    finished: bool
    __counter: int

    enabled: bool
    looped: bool

    def __init__(self,
                 name: str,
                 action_func: typing.Callable[[object, float], None],
                 duration: int,
                 delay: float,
                 value: float,
                 looped: bool):
        self.name = name
        self.action_func = action_func
        self.duration = duration
        self.delay = delay
        self.value = value
        self.__counter = 0
        self.finished = True
        self.enabled = True
        self.looped = looped

    def start(self):
        self.finished = False
        self.__counter = 0

    def update(self, entity: object):
        if self.finished or not self.enabled:
            return
        if self.__counter % self.delay == 0:
            self.action_func(entity, self.value)
        self.__counter += 1
        if self.__counter >= self.duration:
            self.finished = True
            if self.looped:
                self.start()

