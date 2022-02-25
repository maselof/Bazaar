from game_object import *
from enum import Enum
from typing import List
import game_logic
from animation import *
from action import *


class Direction(Enum):
    LEFT = -1
    UP = -1
    RIGHT = 1
    DOWN = 1
    STAND = 0


class Entity(GameObject):
    speed: int
    direction_vector: Vector2
    actions: {Action}
    current_action: Action
    left_flip: bool

    def __init__(self,
                 name: str,
                 speed: int = 10,
                 ):
        super().__init__(name)

        self.speed = speed
        self.direction_vector = Vector2(0, 0)
        self.left_flip = False

        animations_path = 'res/animations/' + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(animations_path + 'Idle', 0.8)),
                        'walking': Action(self.action_walking, Animation(animations_path + 'Walking'))}
        self.current_action = self.actions['idle']

    def set_action(self, key: str, args: [object]):
        self.current_action = self.actions.get(key)
        self.current_action.set_args(args)

    def action_idle(self, args: [object]):
        self.set_direction([Direction.STAND, Direction.STAND])

    def action_walking(self, args: [object]):
        self.set_direction(args[0])
        new_pos = self.get_position() + self.get_direction_vector() * self.speed
        self.set_position(new_pos)

    def set_direction(self, directions: [Direction]):
        self.direction_vector = Vector2(directions[0].value, directions[1].value)
        if directions[0] == Direction.LEFT:
            self.left_flip = True
        elif directions[0] == Direction.RIGHT:
            self.left_flip = False

    def get_direction_vector(self) -> Vector2:
        return self.direction_vector

    def update(self):
        if self.current_action.animation.finished:
            self.current_action.animation.start()
        self.current_action.animation.update()

        self.image = self.current_action.animation.get_current_frame()
        if self.left_flip:
            self.image = pygame.transform.flip(self.image, True, False)

        self.current_action.do()







