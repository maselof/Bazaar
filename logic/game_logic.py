import random

from weapon import Weapon
from item import Item
from pygame import Vector2
from effect import Effect
import pygame
from location import Location
from game_object import GameObject
from entity import *
from chest import Chest


# general
g_timer = 0
g_frames_count = 2
g_fps = 60

exp_gain = 100


# screen
g_screen_width = 1650
g_screen_height = 1000
g_screen_center = Vector2(g_screen_width, g_screen_height) // 2

# objects sizes

# hero
g_hero_width = 30
g_hero_height = 70
hero_take_radius = 85
hero_base_speed = 5
hero_run_speed = 7

# entities
g_entity_walking_anim_speed = 0.2
g_entity_attacking_anim_speed = 0.2
enemy_agro_radius = 300
entity_collision_offset = Vector2(60, 40)
entity_movement_area_size = Vector2(500, 500)

# other
potion_hp = 20
collision_offset = 5

# Inventory
inventory_columns_count = 5
inventory_top_offset = 30
inventory_left_cell_offset = 5
inventory_items_offset = 11
inventory_min_raws_count = 5
inventory_text_size = 16
inventory_background_color = (129, 81, 54)

# Bottom panel
panel_items_count = 10
panel_bottom_offset = 30
panel_items_offset = 11
panel_items_size = 56
panel_number_color = (232, 180, 0)
panel_count_color = (255, 255, 255)
panel_text_size = 16
panel_text_offset = 2

# Dialog window
dw_first_layer_color = (152, 94, 63)
dw_second_layer_color = (185, 122, 87)
dw_text_size = 20
dw_text_color = (255, 255, 255)
dw_layers_offset = 10
dw_text_offset = Vector2(30, 10)
dw_bottom_offset = 200

# Description window
dscw_size = Vector2(300, 300)
dscw_name_text_size = 20
dscw_frame_icon_offset = 5
dscw_description_text_size = 15
dscw_description_offset = 5
dscw_stats_text_size = 20
dscw_cost_text_color = (232, 180, 0)

# message log
ml_text_size = 20
ml_text_color = (255, 255, 255)
ml_duration = 300
ml_left_offset = 30

# interface priorities
hp_bar_priority = 1
inventory_priority = 2
dialog_window_priority = 2
hero_bars_priority = 2
message_log_priority = 2

# hero bars
hb_right_offset = 100
hb_bottom_offset = 50
hb_bar_size = Vector2(250, 15)
hb_health_color = (255, 0, 0)
hb_stamina_color = (0, 255, 0)
hb_mana_color = (0, 0, 255)
hb_frame_color = (0, 0, 0)
hb_bars_offset = 5
hb_text_size = 15
hb_text_color = (232, 180, 0)
hb_exp_bar_color = (255, 255, 255)
hb_exp_text_size = 20

# map
map_frame_size = Vector2(1680, 1050)

# keys

NUMBER_KEYS = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4,
               pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8, pygame.K_0: 9}

# effect funcs:


def healing(entity: object, value: float):
    entity.stats.hp = min(entity.stats.hp + int(value), entity.stats.max_hp)


def bleeding(entity: object, value: float):
    entity.stats.hp = max(entity.stats.hp - int(value), 0)


def fatigue(entity: object, value: float):
    entity.stats.stamina = max(entity.stats.stamina - int(value), 0)


def breathing(entity: object, value: float):
    entity.stats.stamina = min(entity.stats.stamina + int(value), entity.stats.max_stamina)


EFFECTS = {'Healing': Effect('Healing', healing, 1, 1, 10, False),
           'Bleeding': Effect('Bleeding', bleeding, 300, 60, 10, False),
           'Fatigue': Effect('Fatigue', fatigue, 60, 60, 5, True),
           'Breathing': Effect('Breathing', breathing, 60, 60, 5, True)}


def get_effect(id: str) -> Effect:
    effect = EFFECTS.get(id)
    return Effect(effect.name, effect.action_func, effect.duration, effect.delay, effect.value, effect.looped)


# id: GameObject
ITEMS = {}


def init_items():
    ITEMS.update({'heal_potion': Item('heal_potion', 'potions/', Vector2(0, 0), False, 1, [get_effect('Healing')], 20, 'Weak healing potion. Increase your hp on 10 points.'),
                  'fists': Weapon('fists', 40, [], [], 0, ''),
                  'cudgel': Weapon('cudgel', 80, [], [], 100, 'The most common weapon among bandits.'),
                  'sword': Weapon('sword', 120, [], [], 250, 'Some description.')})


def get_item(id: str):
    item = ITEMS.get(id)
    if isinstance(item, Weapon):
        return Weapon(item.name, item.attack_range, item.effects, item.attack_effects, item.cost, item.description)
    return Item(item.name, item.animations_path, item.size, item.directional, item.scaling, item.effects, item.cost, item.description)


ENTITIES = {}


def init_entities():
    skeleton_stats = Stats(max_hp=50, exp=50, lvl=0)
    bandit_stats = Stats(max_hp=100, exp=100, lvl=0)
    ENTITIES.update({'skeleton': Entity('skeleton', '', Vector2(30, 70), entity_collision_offset, 1, skeleton_stats),
                     'bandit': Entity('bandit', '', Vector2(30, 70), entity_collision_offset, 1, bandit_stats)})


def get_entity(id: str):
    entity = ENTITIES.get(id)
    entity_stats = Stats(max_hp=entity.stats.max_hp, exp=entity.stats.exp, lvl=entity.stats.lvl)
    return Entity(entity.name, entity.animations_path, entity.size, entity.collision_rect_offset, entity.scaling, entity_stats)


GAME_OBJECTS = {}


def init_game_objects():
    GAME_OBJECTS.update({'chest': Chest('chest', 'general/', Vector2(58, 5), Vector2(1, 25)),
                         'bag': Chest('bag', 'general/', Vector2(0, 0), Vector2(0, 0))})


def fill_chest(chest: Chest, seed: int):
    items = list(ITEMS.values())
    print(items)
    count = random.randint(0, seed)
    for i in range(count):
        item = items[random.randint(0, len(items) - 1)]
        if item.name != 'fists':
            chest.inventory.add_item(item)


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
                      3: get_meadow})
    LOCATIONS_CHANCES.extend([10, 10, 40, 40])


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

