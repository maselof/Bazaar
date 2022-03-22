import game_logic
from entity import *
from inventory import HeroInventory
from inventory import ILootable
from context import Context
from chest import Chest


class Hero(Entity):

    movement_queue: []
    interact_radius: int
    context: Context
    looting_object: ILootable

    def __init__(self,
                 size: Vector2,
                 collision_rect_offset: pygame.Vector2 = Vector2(0, 0),
                 scaling: float = 1):
        super().__init__('hero', '', size, collision_rect_offset, scaling)
        self.movement_queue = []
        self.interact_radius = game_logic.hero_take_radius
        self.context = Context.GAME
        self.inventory = HeroInventory()
        self.looting_object = None
        self.enable_random_actions = False
        self.speed = 5
        self.ai.is_enemy = False
        self.init_effects()

    def init_effects(self):
        self.effects.update({'Fatigue': game_logic.EFFECTS.get('Fatigue'),
                             'Breathing': game_logic.EFFECTS.get('Breathing')})
        self.effects.get('Fatigue').start()
        self.effects.get('Breathing').start()

    def action_walking(self, args: [object]):
        self.direction_vector = game_cycle.check_collisions(self, args[0][0])
        if len(self.effects):
            if args[0][1] and self.stats.stamina > 0:
                self.speed = game_logic.hero_run_speed
            else:
                self.speed = game_logic.hero_base_speed

            self.actions.get('walking').animation.speed = game_logic.g_entity_walking_anim_speed * self.speed / game_logic.hero_base_speed

            self.effects.get('Fatigue').enabled = args[0][1]
            self.effects.get('Breathing').enabled = False

    def action_idle(self, args: [object]):
        super().action_idle(args)
        if len(self.effects):
            self.effects.get('Fatigue').enabled = False
            self.effects.get('Breathing').enabled = True

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
            self.effects.update({effect.name: effect})
            effect.start()
        if isinstance(item, Weapon):
            new_weapon = game_logic.get_item(item.name)
            new_weapon.set_equipped(item.is_equipped)
            new_weapon.bottom_panel_index = item.bottom_panel_index
            item.bottom_panel_index = 0
            old_weapon = game_logic.get_item(self.weapon.name)
            old_weapon.bottom_panel_index = self.weapon.bottom_panel_index
            if old_weapon.name != 'fists':
                self.inventory.add_item(old_weapon)
                old_weapon.set_equipped(True)
                self.inventory.remove_item(old_weapon)
            if not new_weapon.is_equipped:
                print('not equipped')
                self.inventory.remove_item(new_weapon)
                new_weapon.set_equipped(True)
                self.inventory.add_item(new_weapon)
                self.set_weapon(new_weapon)
            else:
                print('equipped')
                self.inventory.remove_item(new_weapon)
                self.set_weapon(game_logic.get_item('fists'))
            self.inventory.update_panel()
            return

        self.inventory.remove_item(item)

    def change_context(self, context: Context):
        if context == Context.GAME:
            self.inventory.close()
            if self.looting_object:
                self.looting_object.close()
        elif context == Context.INVENTORY:
            self.inventory.open()
            if self.looting_object:
                self.looting_object.inventory.show_frame = False
        elif context == Context.LOOTING:
            self.looting_object.open()
            self.inventory.show_frame = False
        self.context = context

    def interact(self):
        object, distance = game_cycle.get_nearest_object(self)
        if distance > self.interact_radius:
            object = None
            # return

        print(object)
        if isinstance(object, Item):
            self.inventory.add_item(object, object.count)
            game_cycle.game_map.remove_game_object(object)
        elif isinstance(object, Chest):
            if (self.looting_object is not None) and self.looting_object.inventory.is_open:
                self.looting_object.inventory.close()
                if self.inventory.is_open:
                    self.change_context(Context.INVENTORY)
                else:
                    self.change_context(Context.GAME)
            else:
                self.looting_object = object
                self.change_context(Context.LOOTING)

    def die(self):
        pass

    def gain_exp(self, exp: int):
        self.stats.exp += exp
        while self.stats.exp >= self.stats.max_exp:
            self.stats.lvl += 1
            self.stats.exp -= self.stats.max_exp
            self.stats.max_exp += game_logic.exp_gain

    def update(self):
        super().update()
        self.inventory.show_frame = self.context == Context.INVENTORY
        self.check_looting_object_distance()


