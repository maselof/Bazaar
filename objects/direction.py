from enum import Enum
from pygame import Vector2


class Direction(Enum):
    LEFT = Vector2(-1, 0)
    UP = Vector2(0, -1)
    RIGHT = Vector2(1, 0)
    DOWN = Vector2(0, 1)
    STAND = Vector2(0, 0)

