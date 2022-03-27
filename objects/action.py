import typing

from animation import *


class Action:
    func: typing.Callable[[[object]], None]
    animation: Animation
    args: [object]

    def __init__(self,
                 func: typing.Callable[[[object]], None],
                 animation: Animation):
        self.func = func
        self.animation = animation
        self.args = []

    def set_args(self, *args: object):
        self.args = args

    def do(self):
        return self.func(self.args)
