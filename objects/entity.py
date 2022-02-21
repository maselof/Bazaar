from GameForMIREA1.objects.game_object import *
from enum import Enum
from typing import List
from GameForMIREA1.logic import game_logic
from GameForMIREA1.objects.vector2 import *


class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Entity(GameObject):
    speed: int
    direction: Direction
    direction_vector: Vector2
    animations: [pygame.surface.Surface]

    def __init__(self,
                 speed: int = 1,
                 direction: Direction = Direction.LEFT,
                 animations: [pygame.surface.Surface] = []):
        super().__init__()
        self.speed = speed
        self.set_direction(direction)
        self.animations = animations

    def get_direction(self) -> Direction:
        return self.direction

    def set_direction(self, direction: Direction):
        self.direction = direction
        if (self.direction == Direction.LEFT):
            self.direction_vector =  Vector2(-1, 0)
        elif (self.direction == Direction.UP):
            self.direction_vector = Vector2(0, -1)
        elif (self.direction == Direction.RIGHT):
            self.direction_vector = Vector2(1, 0)
        elif (self.direction == Direction.DOWN):
            self.direction_vector = Vector2(0, 1)

    def get_direction_vector(self) -> Vector2:
        return self.direction_vector

    def update(self):
        self.image = self.animations[self.direction.value * game_logic.frames_count +
                                     game_logic.g_timer * game_logic.frames_count // (60)]
        new_pos = Point(self.get_position().x + self.direction_vector.x * self.speed,
                        self.get_position().y + self.direction_vector.y * self.speed)
        self.set_position(new_pos)



