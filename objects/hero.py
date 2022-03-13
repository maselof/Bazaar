import game_logic
from entity import *
from inventory import HeroInventory
from inventory import ILootable
from context import Context


class Hero(Entity):

    movement_queue: []
    interact_radius: int
    context: Context
    looting_object: ILootable

    def __init__(self,
                 size: Vector2,
                 scaling: float = 1):
        super().__init__('hero', '', size, scaling)
        self.movement_queue = []
        self.interact_radius = game_logic.hero_take_radius
        self.context = Context.GAME
        self.inventory = HeroInventory()
        self.looting_object = None
        self.enable_random_actions = False
        self.speed = 5
        self.ai.is_enemy = False

    def action_walking(self, args: [object]):
        self.direction_vector = game_cycle.check_collisions(self, args[0])

    def check_looting_object_distance(self):
        if not self.looting_object:
            return
        if game_cycle.get_distance(self, self.looting_object) > self.interact_radius:
            if self.inventory.is_open:
                self.change_context(Context.INVENTORY)
            else:
                self.change_context(Context.GAME)
            self.looting_object.inventory.close()
            self.looting_object = None

    def use(self, item: Item):
        for effect in item.effects:
            self.effects.append(effect)
            effect.start()
        if isinstance(item, Weapon):
            old_weapon = self.weapon
            self.set_weapon(item)
            if old_weapon.name != 'fists':
                self.inventory.add_item(old_weapon)
        self.inventory.remove_item(item)

    def change_context(self, context: Context):
        if context == Context.GAME:
            self.inventory.close()
            if self.looting_object:
                self.looting_object.inventory.close()
        elif context == Context.INVENTORY:
            self.inventory.is_open = True
            self.inventory.show_frame = True
            if self.looting_object:
                self.looting_object.inventory.show_frame = False
        elif context == Context.LOOTING:
            self.looting_object.inventory.is_open = True
            self.looting_object.inventory.show_frame = True
            self.inventory.show_frame = False
        self.context = context

    def interact(self):
        object, distance = game_cycle.get_nearest_object(self)
        if distance > self.interact_radius:
            object = None

        print(object)
        if isinstance(object, Item):
            self.inventory.add_item(object)
            game_cycle.game_map.game_objects.remove(object)
        elif isinstance(object, Entity):
            if (self.looting_object != None) and self.looting_object.inventory.is_open:
                self.looting_object.inventory.close()
                if self.inventory.is_open:
                    self.change_context(Context.INVENTORY)
                else:
                    self.change_context(Context.GAME)
            else:
                self.looting_object = object
                self.change_context(Context.LOOTING)

    def update(self):
        super().update()
        self.inventory.show_frame = self.context == Context.INVENTORY
        self.check_looting_object_distance()


