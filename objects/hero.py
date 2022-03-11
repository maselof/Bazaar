import game_logic
from entity import *
from inventory import HeroInventory
from context import Context


class Hero(Entity):

    movement_queue: []
    take_radius: int
    context: Context

    def __init__(self,
                 size: Vector2,
                 scaling: float = 1):
        super().__init__('hero', '', size, scaling)
        self.movement_queue = []
        self.take_radius = game_logic.hero_take_radius
        self.context = Context.GAME
        self.inventory = HeroInventory()

    def action_walking(self, args: [object]):
        self.direction_vector = args[0]

    def interact(self):
        object, distance = game_cycle.get_nearest_object(self)
        if distance > self.take_radius:
            object = None

        print(object)
        if isinstance(object, Item):
            self.inventory.add_item(object)
            game_cycle.game_map.game_objects.remove(object)
        elif isinstance(object, Entity):
            self.inventory.show = True
            object.inventory.show = True
            self.context = Context.LOOTING

    def update(self):
        super().update()
        self.inventory.show_frame = self.context == Context.INVENTORY


