from weapon import Weapon
from item import Item
from pygame import Vector2
from effect import Effect
import pygame


# general
g_timer = 0
g_frames_count = 2
g_fps = 60


# screen
g_screen_width = 1680
g_screen_height = 1000
g_screen_center = Vector2(g_screen_width, g_screen_height) // 2

# objects sizes

# hero
g_hero_width = 30
g_hero_height = 70
hero_take_radius = 50

# entities
g_entity_walking_anim_speed = 0.2
g_entity_attacking_anim_speed = 0.2
enemy_agro_radius = 100
entity_collision_offset = Vector2(60, 40)

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
draw_inventory = False

# Bottom panel
panel_items_count = 10
panel_bottom_offset = 30
panel_items_offset = 11
panel_items_size = 56

# Dialog window
dw_first_layer_color = (152, 94, 63)
dw_second_layer_color = (185, 122, 87)
dw_text_size = 20
dw_text_color = (255, 255, 255)
dw_layers_offset = 10
dw_text_offset = Vector2(30, 10)
dw_bottom_offset = 200

# interface priorities
hp_bar_priority = 1
inventory_priority = 2
dialog_window_priority = 2

# map
map_frame_size = Vector2(1680, 1050)

# effect funcs:


def healing(entity: object):
    entity.hp += potion_hp


def bleeding(entity: object):
    entity.hp -= 10


EFFECTS = {'Healing': Effect('Healing', healing, 1, 1),
           'Bleeding': Effect('Bleeding', bleeding, 300, 60)}


def get_effect(id: str) -> Effect:
    effect = EFFECTS.get(id)
    return Effect(effect.name, effect.action_func, effect.duration, effect.delay)


# id: GameObject
ITEMS = {'heal_potion': Item('heal_potion', 'potions/', Vector2(0, 0), False, 1, [get_effect('Healing')]),
         'fists': Weapon('fists', 40, [], []),
         'cudgel': Weapon('cudgel', 80, [], [])}


def get_item(id: str):
    item = ITEMS.get(id)
    if isinstance(item, Weapon):
        return Weapon(item.name, item.attack_range, item.effects, item.attack_effects)
    return Item(item.name, item.animations_path, item.size, item.directional, item.scaling, item.effects)


def get_text_size(message, font_size=30, font_type="res/fonts/a_Alterna.ttf") -> Vector2:
    font = pygame.font.Font(font_type, font_size)
    return Vector2(font.size(message))


def print_text(screen, message, x, y, font_color=(0, 0, 0), font_type="res/fonts/a_Alterna.ttf", font_size=30):

    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

