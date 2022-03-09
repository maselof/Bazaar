import game_logic
from entity import *


class Hero(Entity):

    movement_queue: []

    def __init__(self,
                 size: Vector2,
                 scaling: float = 1):
        super().__init__('hero', '', size, scaling)
        self.movement_queue = []

    def action_walking(self, args: [object]):
        self.direction_vector = args[0]

