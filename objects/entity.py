from game_object import *
from enum import Enum
from action import *
from pygame.math import Vector2


class Direction(Enum):
    LEFT = -1
    UP = -1
    RIGHT = 1
    DOWN = 1
    STAND = 0


class Entity(GameObject):
    speed: int
    direction_vector: Vector2
    left_flip: bool

    max_hp: int
    hp: int

    def __init__(self,
                 name: str,
                 animations_path: str = '',
                 scaling: float = 1
                 ):
        super().__init__(name, animations_path, scaling)

        self.speed = 5
        self.direction_vector = Vector2(0, 0)
        self.left_flip = False

        self.max_hp = 100
        self.hp = 100

    def animations_init(self):
        path = 'res/animations/entities/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path + 'Idle')),
                        'walking': Action(self.action_walking, Animation(path + 'Walking')),
                        'attacking': Action(self.action_attacking, Animation(path + 'Attacking', False))}
        self.current_action = self.actions['idle']

    def action_idle(self, args: [object]):
        super().action_idle(args)
        self.set_direction([Direction.STAND, Direction.STAND])

    def action_walking(self, args: [object]):
        self.set_direction(args[0])
        new_pos = self.get_position() + self.get_direction_vector() * self.speed
        self.set_position(new_pos)

    def action_attacking(self, args: [object]):
        pass

    def set_direction(self, directions: [Direction]):
        self.direction_vector = Vector2(directions[0].value, directions[1].value)
        if directions[0] == Direction.LEFT:
            self.left_flip = True
        elif directions[0] == Direction.RIGHT:
            self.left_flip = False

    def get_direction_vector(self) -> Vector2:
        return self.direction_vector

    def update(self):
        super().update()
        if self.left_flip:
            self.image = pygame.transform.flip(self.image, True, False)







