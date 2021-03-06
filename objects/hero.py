import pygame
from pygame import Vector2

import game_logic
import game_cycle
from entity import Entity
from inventory import HeroInventory
from inventory import ILootable
from context import Context
from chest import Chest
from item import Item
from weapon import Weapon
from sound_wrapper import SoundWrapper


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
        self.interact_radius = game_logic.HERO_INTERACT_RADIUS
        self.context = Context.GAME
        self.inventory = HeroInventory()
        self.looting_object = None
        self.enable_random_actions = False
        self.ai.is_enemy = False
        self.init_effects()
        self.scale_sounds(1)

    def init_effects(self):
        self.effects.update({'Fatigue': game_logic.EFFECTS.get('Fatigue'),
                             'Breathing': game_logic.EFFECTS.get('Breathing')})
        self.effects.get('Fatigue').start()
        self.effects.get('Breathing').start()

    def sounds_init(self):
        super().sounds_init()
        self.sounds.update({'OpenInv': SoundWrapper('res/sounds/entities/hero/openInv.mp3', True, 1),
                            'CloseInv': SoundWrapper('res/sounds/entities/hero/closeInv.mp3', True, 1)})

    def set_weapon(self, weapon: Weapon):
        super().set_weapon(weapon)
        self.weapon.scale_sounds(1)

    def action_walking(self, args: [object]):
        self.direction_vector = game_cycle.game_data.game_map.check_collisions(self, args[0][0])
        if len(self.effects):
            self.stats.movement_speed = int(self.stats.dexterity / 10 * game_logic.HERO_BASE_SPEED)
            if args[0][1] and self.stats.stamina > 0:
                self.stats.movement_speed = int(self.stats.movement_speed * 1.5)

            self.actions.get('walking').animation.speed = (game_logic.ENTITY_WALKING_ANIM_SPEED *
                                                           self.stats.movement_speed / game_logic.HERO_BASE_SPEED)
            self.effects.get('Fatigue').enabled = args[0][1]
            self.effects.get('Breathing').enabled = False
        if self.sounds:
            self.sounds.get('Steps').play(-1)

    def action_idle(self, args: [object]):
        super().action_idle(args)
        if len(self.effects):
            self.effects.get('Fatigue').enabled = False
            self.effects.get('Breathing').enabled = True

    def get_coins_count(self):
        for item in self.inventory.container:
            if item.name == 'coin':
                return item.count
        return 0

    def check_looting_object_distance(self):
        if not self.looting_object:
            return
        if game_cycle.game_data.game_map.get_distance(self, self.looting_object) > self.interact_radius:
            if self.inventory.is_open:
                self.change_context(Context.INVENTORY)
            else:
                self.change_context(Context.GAME)
            self.looting_object.inventory.close()
            self.looting_object = None

    def use(self, item: Item):
        if item.name == 'coin':
            return

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
                self.inventory.remove_item(new_weapon)
                new_weapon.set_equipped(True)
                self.inventory.add_item(new_weapon)
                self.set_weapon(new_weapon)
            else:
                self.inventory.remove_item(new_weapon)
                self.set_weapon(game_logic.get_item('fists'))
            self.inventory.update_panel()
            return

        self.inventory.remove_item(item)

    def change_context(self, context: Context):
        if (self.context == Context.MENU or self.context == Context.START) and context != Context.GAME:
            return

        if self.context == Context.START:
            pygame.mixer.stop()
            pygame.mixer.Sound('res/sounds/general/background.mp3').play(-1)

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
        elif context == Context.SKILLS:
            pass
        elif context == Context.DEATH:
            pygame.mixer.stop()
            pygame.mixer.Sound('res/sounds/general/death.mp3').play(-1)
        elif context == Context.START:
            pygame.mixer.stop()
            pygame.mixer.Sound('res/sounds/general/menu.mp3').play(-1)
        self.context = context

    def interact(self):
        object, distance = game_cycle.game_data.game_map.get_nearest_object(self)
        if distance > self.interact_radius:
            return

        if isinstance(object, Item):
            self.inventory.add_item(object, object.count)
            game_cycle.game_data.game_map.remove_game_object(object)
            game_cycle.game_data.message_log.add_message(f'Looted {object.name} x{object.count}')
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
            self.stats.skill_points += 1
            self.stats.exp -= self.stats.max_exp
            self.stats.max_exp += game_logic.LVL_EXP_STEP
            self.refresh()
            game_cycle.game_data.message_log.add_message('LVL UP!')

    def update(self):
        super().update()
        self.inventory.show_frame = self.context == Context.INVENTORY
        self.check_looting_object_distance()
        if self.stats.hp <= 0:
            self.change_context(Context.DEATH)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
