import random
from enum import Enum

from pygame import Vector2


class Direction(Enum):
    LEFT = Vector2(-1, 0)
    UP = Vector2(0, -1)
    RIGHT = Vector2(1, 0)
    DOWN = Vector2(0, 1)
    STAND = Vector2(0, 0)


def is_horizontal(direction: Direction):
    return direction == Direction.LEFT or direction == Direction.RIGHT


def get_random_direction() -> Direction:
    value = random.randint(0, 4)
    match value:
        case 0:
            return Direction.LEFT
        case 1:
            return Direction.UP
        case 2:
            return Direction.RIGHT
        case 3:
            return Direction.DOWN
        case 4:
            return Direction.STAND
