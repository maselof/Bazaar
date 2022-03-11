from weapon import Weapon
from item import Item
from pygame import Vector2
from effect import Effect


# general
g_timer = 0
g_frames_count = 2
g_fps = 60


# screen
g_screen_width = 1680
g_screen_height = 1000

# objects sizes

# hero
g_hero_width = 30
g_hero_height = 70
hero_take_radius = 50

# entities
g_entity_walking_anim_speed = 0.2
g_entity_attacking_anim_speed = 0.2

# other
potion_hp = 20

# Inventory
inventory_columns_count = 5
inventory_top_offset = 30
inventory_left_cell_offset = 5
inventory_items_offset = 11
inventory_min_raws_count = 5

# Bottom panel
panel_items_count = 10
panel_bottom_offset = 30
panel_items_offset = 11
panel_items_size = 56


# effect funcs:

def healing(entity: object):
    entity.hp += potion_hp


EFFECTS = {0: Effect('Healing', healing, 1, 0)}


def get_effect(id: int) -> Effect:
    return EFFECTS.get(id)


# id: GameObject
ITEMS = {0: Item('heal_potion', 'potions/', Vector2(0, 0), False, 1, [get_effect(0)]),
         1: Weapon('fists', 30, [], []),
         2: Weapon('cudgel', 80, [], [])}


def get_item(id: int):
    return ITEMS.get(id)






draw_inventory = False
