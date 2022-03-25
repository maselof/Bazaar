from location import Location
from entity import *
from chest import Chest
from trader import Trader


# general
g_frames_count = 2
g_fps = 60

exp_gain = 100


# screen
g_screen_width = 1680
g_screen_height = 1050
g_screen_center = Vector2(g_screen_width, g_screen_height) // 2

# menu
menu_width = 400
menu_buttons_offset = 20
menu_buttons_text_size = 30
menu_active_button_color = (255, 255, 255)
menu_inactive_button_color = (232, 180, 0)
menu_first_layer_color = (152, 94, 63)
menu_second_layer_color = (185, 122, 87)
menu_layers_offset = 10

# death message
dm_size = Vector2(400, 100)

# hero
g_hero_width = 30
g_hero_height = 70
hero_take_radius = 85
hero_base_speed = 5
hero_sounds_range = 500

# entities
g_entity_walking_anim_speed = 0.2
g_entity_attacking_anim_speed = 0.2
enemy_agro_radius = 300
entity_collision_offset = Vector2(60, 40)
entity_movement_area_size = Vector2(500, 500)

# skills panel
sp_width = 400
sp_first_layer_color = (152, 94, 63)
sp_second_layer_color = (185, 122, 87)
sp_layers_offset = 10
sp_text_size = 20
sp_text_color = (255, 255, 255)
sp_border_size = 2
sp_border_color = (255, 255, 255)
sp_text_offset = 5
sp_arrow_offset = Vector2(2, 3)

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

# health bar
hb_lvl_text_size = 15

# interface priorities
hp_bar_priority = 1
inventory_priority = 2
dialog_window_priority = 2
hero_bars_priority = 2
message_log_priority = 2
skills_panel_priority = 3

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


def mana_recovery(entity: object, value: float):
    entity.stats.mana = min(entity.stats.mana + int(value), entity.stats.max_mana)


def refreshing(entity: object, value: float):
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

pygame.init()

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

                  'golden_potion': Item('golden_potion', 'potions/', Vector2(0, 0), False, 1, [get_effect('Refresh')], 500,
                                      'Golden potion. Recovery all stats.', 10),

                  'cudgel': Weapon('cudgel', 40, 0.7, 80, [], [], 100, 'The most common weapon among bandits.', 10),
                  'sword': Weapon('sword', 20, 1.5, 120, [], [], 250, 'Some description.', 10),
                  'axe': Weapon('axe', 30, 0.8, 60, [], [], 150, 'Axe.', 10)})


def get_item(id: str):
    item = ITEMS.get(id)
    if isinstance(item, Weapon):
        return Weapon(item.name, item.damage, item.attack_speed_modifier, item.attack_range, item.effects, item.attack_effects, item.cost, item.description, item.trading_count)
    return Item(item.name, item.animations_path, item.size, item.directional, item.scaling, item.effects, item.cost, item.description, item.trading_count)


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
    count = random.randint(0, seed)
    for i in range(count):
        item = items[random.randint(0, len(items) - 1)]
        if item.name != 'fists':
            chest.inventory.add_item(item)
    gold = random.randint(0, seed * 100)
    chest.inventory.add_item(game_logic.get_item('coin'), gold)


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
