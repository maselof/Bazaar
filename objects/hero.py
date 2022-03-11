import game_logic
from entity import *
from inventory import HeroInventory


class Hero(Entity):

    movement_queue: []
    take_radius: int

    def __init__(self,
                 size: Vector2,
                 scaling: float = 1):
        super().__init__('hero', '', size, scaling)
        self.movement_queue = []
        self.take_radius = game_logic.hero_take_radius
        self.inventory = HeroInventory()

    def action_walking(self, args: [object]):
        self.direction_vector = args[0]

    def take(self):
        object, distance = game_cycle.get_nearest_object(self)
        if distance > self.take_radius:
            object = None
        print(object)

