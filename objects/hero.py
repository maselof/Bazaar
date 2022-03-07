import game_logic
from entity import *


class Hero(Entity):

    movement_queue: []

    def __init__(self,
                 scaling: float = 1):
        super().__init__('hero', '', scaling)
        self.rect.size = [int(game_logic.g_hero_width * scaling),
                          int(game_logic.g_hero_height * scaling)]
        self.movement_queue = []

    def action_walking(self, args: [object]):
        self.direction_vector = args[0]
