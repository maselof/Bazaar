from objects.point import *


class Vector2(Point):
    def __init__(self,
                 x: int = 0,
                 y: int = 0):
        super().__init__(x, y)