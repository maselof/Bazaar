import random

import pygame.display
from pygame import Vector2

from location import Location
from entity import Entity
from entity import Stats
from chest import Chest
from trader import Trader
from effect import Effect
from weapon import Weapon
from item import Item
from game_object import GameObject


# general
FPS = 60
LVL_EXP_STEP = 100
COLLISION_OFFSET = 5

# screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_CENTER = Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) // 2

# menu
MENU_WIDTH = 400
MENU_BUTTONS_OFFSET = 20
MENU_BUTTONS_TEXT_SIZE = 30
MENU_ACTIVE_BUTTON_COLOR = (255, 255, 255)
MENU_INACTIVE_BUTTON_COLOR = (232, 180, 0)
MENU_FIRST_LAYER_COLOR = (152, 94, 63)
MENU_SECOND_LAYER_COLOR = (185, 122, 87)
MENU_LAYERS_OFFSET = 10

# death message
DM_SIZE = Vector2(400, 100)

# hero
HERO_WIDTH = 30
HERO_HEIGHT = 70
HERO_INTERACT_RADIUS = 85
HERO_BASE_SPEED = 5
HERO_SOUNDS_RANGE = 500

# entities
ENTITY_WALKING_ANIM_SPEED = 0.2
ENTITY_ATTACKING_ANIM_SPEED = 0.2
ENEMY_AGRO_RADIUS = 300
ENTITY_COLLISION_OFFSET = Vector2(60, 40)
ENTITY_MOVEMENT_AREA_SIZE = Vector2(500, 500)

# skills panel
SP_WIDTH = 400
SP_FIRST_LAYER_COLOR = (152, 94, 63)
SP_SECOND_LAYER_COLOR = (185, 122, 87)
SP_LAYERS_OFFSET = 10
SP_TEXT_SIZE = 20
SP_TEXT_COLOR = (255, 255, 255)
SP_BORDER_SIZE = 2
SP_BORDER_COLOR = (255, 255, 255)
SP_TEXT_OFFSET = 5
SP_ARROW_OFFSET = Vector2(2, 3)

# Inventory
INVENTORY_COLUMNS_COUNT = 5
INVENTORY_TOP_OFFSET = 30
INVENTORY_LEFT_CELL_OFFSET = 5
INVENTORY_ITEMS_OFFSET = 11
INVENTORY_MIN_RAWS_COUNT = 5
INVENTORY_TEXT_SIZE = 16
INVENTORY_BACKGROUND_COLOR = (129, 81, 54)

# Bottom panel
PANEL_ITEMS_COUNT = 10
PANEL_BOTTOM_OFFSET = 30
PANEL_ITEMS_OFFSET = 11
PANEL_ITEMS_SIZE = 56
PANEL_NUMBER_COLOR = (232, 180, 0)
PANEL_COUNT_COLOR = (255, 255, 255)
PANEL_TEXT_SIZE = 16
PANEL_TEXT_OFFSET = 2

# Dialog window
DW_FIRST_LAYER_COLOR = (152, 94, 63)
DW_SECOND_LAYER_COLOR = (185, 122, 87)
DW_TEXT_SIZE = 20
DW_TEXT_COLOR = (255, 255, 255)
DW_LAYERS_OFFSET = 10
DW_TEXT_OFFSET = Vector2(30, 10)
DW_BOTTOM_OFFSET = 200

# Description window
DSCW_SIZE = Vector2(300, 300)
DSCW_NAME_TEXT_SIZE = 20
DSCW_FRAME_ICON_OFFSET = 5
DSCW_DESCRIPTION_TEXT_SIZE = 15
DSCW_DESCRIPTION_OFFSET = 5
DSCW_STATS_TEXT_SIZE = 20
DSCW_COST_TEXT_COLOR = (232, 180, 0)

# message log
ML_TEXT_SIZE = 20
ML_TEXT_COLOR = (255, 255, 255)
ML_DURATION = 300
ML_LEFT_OFFSET = 30

# health bar
HB_LVL_TEXT_SIZE = 15

# interface priorities
HP_BAR_PRIORITY = 1
INVENTORY_PRIORITY = 2
DIALOG_WINDOW_PRIORITY = 2
HERO_BARS_PRIORITY = 2
MESSAGE_LOG_PRIORITY = 2
SKILLS_PANEL_PRIORITY = 3

# hero bars
HB_RIGHT_OFFSET = 100
HB_BOTTOM_OFFSET = 50
HB_BAR_SIZE = Vector2(250, 15)
HB_HEALTH_COLOR = (255, 0, 0)
HB_STAMINA_COLOR = (0, 255, 0)
HB_MANA_COLOR = (0, 0, 255)
HB_FRAME_COLOR = (0, 0, 0)
HB_BARS_OFFSET = 5
HB_TEXT_SIZE = 15
HB_TEXT_COLOR = (232, 180, 0)
HB_EXP_BAR_COLOR = (255, 255, 255)
HB_EXP_TEXT_SIZE = 20

# map
MAP_FRAME_SIZE = Vector2(1680, 1050)

# keys

NUMBER_KEYS = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4,
               pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8, pygame.K_0: 9}

# effect funcs:

pygame.init()
pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


def healing(entity, value: float):
    entity.stats.hp = min(entity.stats.hp + int(value), entity.stats.max_hp)


def bleeding(entity, value: float):
    entity.stats.hp = max(entity.stats.hp - int(value), 0)


def fatigue(entity, value: float):
    entity.stats.stamina = max(entity.stats.stamina - int(value), 0)


def breathing(entity, value: float):
    entity.stats.stamina = min(entity.stats.stamina + int(value), entity.stats.max_stamina)


def mana_recovery(entity, value: float):
    entity.stats.mana = min(entity.stats.mana + int(value), entity.stats.max_mana)


def refreshing(entity, value: float):
    entity.stats.hp = entity.stats.max_hp
    entity.stats.stamina = entity.stats.max_stamina
    entity.stats.mana = entity.stats.max_mana


EFFECTS = {'Healing': Effect('Healing', healing, 1, 1, 50, False),
           'Bleeding': Effect('Bleeding', bleeding, 300, 60, 10, False),
           'Fatigue': Effect('Fatigue', fatigue, 30, 30, 5, True),
           'Breathing': Effect('Breathing', breathing, 60, 60, 5, True),
           'Weak Mana Recovery': Effect('Mana Recovery', mana_recovery, 1, 1, 50, False),
           'Mean Mana Recovery': Effect('Mana Recovery', mana_recovery, 1, 1, 100, False),
           'Weak Stamina Recovery': Effect('Stamina Recovery', breathing, 1, 1, 50, False),
           'Mean Stamina Recovery': Effect('Stamina Recovery', breathing, 1, 1, 100, False),
           'Refresh': Effect('All stats recovery', refreshing, 1, 1, 10000, False)}


def get_effect(id: str) -> Effect:
    effect = EFFECTS.get(id)
    return Effect(effect.name, effect.action_func, effect.duration, effect.delay, effect.value, effect.looped)


# id: GameObject
ITEMS = {'fists': Weapon('fists', 10, 1, 50, [], [], 0, '', 0)}


def init_items():
    ITEMS.update({'coin': Item('coin', 'general/', Vector2(0, 0), False, 1, [], 1, 'Gold coin.', 0),

                  'heal_potion': Item('heal_potion', 'potions/', Vector2(0, 0), False, 1, [get_effect('Healing')], 20,
                                      'Weak healing potion. Increase your hp on 50 points.', 50),

                  'endurance_potion': Item('endurance_potion', 'potions/', Vector2(0, 0), False, 1,
                                           [get_effect('Weak Stamina Recovery')], 20,
                                           'Weak stamina potion. Increase your sp on 50 points.', 50),

                  'endurance_potion_2': Item('endurance_potion_2', 'potions/', Vector2(0, 0), False, 1,
                                             [get_effect('Mean Stamina Recovery')], 40,
                                             'Mean stamina potion. Increase your sp on 100 points.', 50),

                  'mana_potion': Item('mana_potion', 'potions/', Vector2(0, 0), False, 1,
                                      [get_effect('Weak Mana Recovery')], 20,
                                      'Weak mana potion. Increase your mp on 50 points.', 50),

                  'mana_potion_2': Item('mana_potion_2', 'potions/', Vector2(0, 0), False, 1,
                                        [get_effect('Mean Mana Recovery')], 40,
                                        'Mean mana potion. Increase your mp on 100 points.', 50),

                  'golden_potion': Item('golden_potion', 'potions/', Vector2(0, 0), False, 1, [get_effect('Refresh')],
                                        500, 'Golden potion. Recovery all stats.', 10),

                  'cudgel': Weapon('cudgel', 40, 0.7, 80, [], [], 100, 'The most common weapon among bandits.', 10),
                  'sword': Weapon('sword', 20, 1.5, 120, [], [], 250, 'Some description.', 10),
                  'axe': Weapon('axe', 30, 0.8, 60, [], [], 150, 'Axe.', 10)})


def get_item(id: str):
    item = ITEMS.get(id)
    if isinstance(item, Weapon):
        return Weapon(item.name, item.damage, item.attack_speed_modifier, item.attack_range, item.effects,
                      item.attack_effects, item.cost, item.description, item.trading_count)
    return Item(item.name, item.animations_path, item.size, item.directional, item.scaling,
                item.effects, item.cost, item.description, item.trading_count)


def get_weapons():
    weapons = []
    for id in ITEMS.keys():
        item = get_item(id)
        if isinstance(item, Weapon):
            weapons.append(item)
    return weapons


ENTITIES = {}


def init_entities():
    skeleton_stats = Stats(max_hp=50, exp=50, lvl=0)
    bandit_stats = Stats(max_hp=100, exp=100, lvl=0)
    ENTITIES.update({'skeleton': Entity('skeleton', '', Vector2(30, 70), ENTITY_COLLISION_OFFSET, 1, skeleton_stats),
                     'bandit': Entity('bandit', '', Vector2(30, 70), ENTITY_COLLISION_OFFSET, 1, bandit_stats)})


def get_entity(id: str):
    entity = ENTITIES.get(id)
    entity_stats = Stats(max_hp=entity.stats.max_hp, exp=entity.stats.exp, lvl=entity.stats.lvl)
    return Entity(entity.name, entity.animations_path, entity.size,
                  entity.collision_rect_offset, entity.scaling, entity_stats)


GAME_OBJECTS = {}


def init_game_objects():
    GAME_OBJECTS.update({'chest': Chest('chest', 'general/', Vector2(58, 5), Vector2(1, 25)),
                         'bag': Chest('bag', 'general/', Vector2(0, 0), Vector2(0, 0))})


def fill_chest(chest: Chest, seed: int):
    items = list(ITEMS.values())
    count = random.randint(0, seed)
    for i in range(count):
        item = items[random.randint(0, len(items) - 1)]
        if item.name != 'fists':
            chest.inventory.add_item(item)
    gold = random.randint(0, seed * 100)
    chest.inventory.add_item(get_item('coin'), gold)


def get_game_object(name: str) -> GameObject:
    go = GAME_OBJECTS.get(name)
    if isinstance(go, Chest):
        cgo = Chest(go.name, go.animations_path, go.size, go.collision_rect_offset)
        return cgo
    return GameObject(go.name, go.animations_path, go.size, go.collision_rect_offset, go.directional, go.scaling)


LOCATIONS = {}
LOCATIONS_CHANCES = []


def get_location(id: int):
    return LOCATIONS.get(id)()


def init_locations():
    LOCATIONS.update({0: get_bandit_camp,
                      1: get_church,
                      2: get_forest,
                      3: get_meadow,
                      4: get_trading_counter})
    LOCATIONS_CHANCES.extend([5, 5, 40, 40, 10])


def get_bandit_camp():
    campfire = GameObject('campfire', 'locations/', Vector2(40, 3), Vector2(5, 20), False, 1)
    campfire.actions.get('idle').animation.speed = 0.4
    campfire.set_position(Vector2(300, 100))
    box = GameObject('box', 'locations/', Vector2(50, 5), Vector2(10, 20), False, 1)
    box.set_position(Vector2(200, 300))
    table = GameObject('table', 'locations/', Vector2(135, 20), Vector2(5, 45), False, 1)
    table.set_position(Vector2(100, 0))
    bandit_camp = Location([campfire, table, box], ['bandit', 'bandit'], Vector2(0, 0), Vector2(500, 500))
    return bandit_camp


def get_church():
    church_building = GameObject('church', 'buildings/', Vector2(315, 320), Vector2(24, 355), False, 1)
    church_building.set_position(Vector2(100, 50))
    church_location = Location([church_building], ['skeleton', 'skeleton'], Vector2(0, 0), Vector2(800, 1000))
    return church_location


def get_trading_counter():
    trader = Trader(Vector2(148, 16), Vector2(10, 85))
    location = Location([trader], [], Vector2(0, 0), Vector2(200, 200))
    return location


def get_forest():
    return Location([], [], Vector2(0, 0), Vector2(0, 0))


def get_meadow():
    return Location([], [], Vector2(0, 0), Vector2(0, 0))


def get_random_location() -> Location:
    value = random.randint(0, 99)
    id = 0
    border = 0
    for r in LOCATIONS_CHANCES:
        border += r
        if value < border:
            return get_location(id)
        id += 1


def get_text_size(message, font_size=30, font_type="res/fonts/a_Alterna.ttf") -> Vector2:
    font = pygame.font.Font(font_type, font_size)
    return Vector2(font.size(message))


def print_text(screen, message, x, y, font_color=(0, 0, 0), font_type="res/fonts/a_Alterna.ttf", font_size=30):

    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))
