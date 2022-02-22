from game_object import *
from enum import Enum
from typing import List
import game_logic


class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    STAND = 5


class Entity(GameObject):
    speed: int
    direction: Direction
    direction_vector: Vector2
    current_animation_index: int

    def __init__(self,
                 speed: int = 1,
                 direction: Direction = Direction.LEFT,
                 ):
        super().__init__()
        self.speed = speed
        self.set_direction(direction)
        self.current_animation_index = 0

    def get_direction(self) -> Direction:
        return self.direction

    def set_direction(self, direction: Direction):
        self.direction = direction
        if self.direction == Direction.LEFT:
            self.direction_vector = Vector2(-1, 0)
        elif self.direction == Direction.UP:
            self.direction_vector = Vector2(0, -1)
        elif self.direction == Direction.RIGHT:
            self.direction_vector = Vector2(1, 0)
        elif self.direction == Direction.DOWN:
            self.direction_vector = Vector2(0, 1)
        elif self.direction == Direction.STAND:
            self.direction_vector = Vector2(0, 0)

    def get_direction_vector(self) -> Vector2:
        return self.direction_vector

    def update(self):
        if self.direction != Direction.STAND:
            self.image = self.animations[self.direction.value * game_logic.g_frames_count +
                                         game_logic.g_timer * game_logic.g_frames_count // (60)]
        new_pos = self.get_position() + self.get_direction_vector() * self.speed
        self.set_position(new_pos)



