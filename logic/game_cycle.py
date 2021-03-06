import sys
import pickle

import pygame
from pygame import Vector2

import game_logic
import interface
from context import Context
from map import Map
from hero import Hero
from camera import Camera
from trader import Trader
from direction import Direction
from direction import is_horizontal
from weapon import Weapon


class GameData:
    hero: Hero
    game_interface: interface.Interface
    game_map: Map
    camera: Camera
    message_log: interface.MessageLog
    skills_panel: interface.SkillsPanel
    dialog_window: interface.DialogWindow
    menu: interface.Menu

    def __init__(self):
        self.menu = interface.Menu()

    def init(self):
        self.game_interface = interface.Interface()
        self.create_hero()
        self.message_log = interface.MessageLog()
        self.skills_panel = interface.SkillsPanel(self.hero)
        self.dialog_window = interface.DialogWindow(self.hero)

        game_logic.init_items()
        game_logic.init_game_objects()
        game_logic.init_entities()
        game_logic.init_locations()

        hero_weapon = game_logic.get_item('fists')
        self.hero.set_weapon(hero_weapon)
        self.hero.inventory.add_item(game_logic.get_item('heal_potion'), 10)

        self.game_map = Map(self.hero)
        self.camera = Camera(self.game_map, self.hero)

        self.game_interface.add_element(interface.HeroBars(self.hero))
        self.game_interface.add_element(self.hero.inventory)
        self.game_interface.add_element(self.message_log)
        self.game_interface.add_element(self.skills_panel)
        self.game_interface.add_element(self.dialog_window)
        self.game_map.add_game_object(self.hero)

    def create_hero(self):
        hero = Hero(Vector2(game_logic.HERO_WIDTH, game_logic.HERO_HEIGHT), game_logic.ENTITY_COLLISION_OFFSET)
        hero.update()
        hero_width, hero_height = hero.image.get_size()
        center = Vector2((game_logic.SCREEN_WIDTH - hero_width) // 2,
                         (game_logic.SCREEN_HEIGHT - hero_height) // 2)
        hero.set_position(center)
        self.hero = hero

    def update(self):
        self.game_map.update()
        self.camera.update()
        self.game_interface.update()

    def draw(self, screen: pygame.Surface):
        self.game_map.draw(screen)
        self.game_interface.draw(screen)


game_data = GameData()


def save(name: str):
    with open(f"saves/{name}.SAV", "wb") as f:
        pickle.dump(game_data, f)
        game_data.message_log.add_message('Saved!')


def load(name: str):
    with open(f"saves/{name}.SAV", "rb") as f:
        global game_data
        for go in game_data.game_map.all_game_objects:
            go.scale_sounds(0)
        game_data = pickle.load(f)
        game_data.hero.movement_queue = []
        game_data.hero.scale_sounds(1)
        game_data.message_log.add_message('Loaded!')


def remove_all_directions(queue: [Direction], direction: Direction):
    for i in range(queue.count(direction)):
        queue.remove(direction)


def handle_movement(hero, switch_mode: bool):

    direction_vector = Vector2(0, 0)
    priority_direction = hero.direction

    reversed_queue = hero.movement_queue.copy()
    reversed_queue.reverse()

    if not len(reversed_queue):
        hero.set_action('idle', None)
        return

    if reversed_queue[0]:
        priority_direction = reversed_queue[0]

    hero.direction = priority_direction
    direction_vector += priority_direction.value

    for direction in reversed_queue:
        if is_horizontal(priority_direction):
            if not is_horizontal(direction):
                direction_vector += direction.value
                break
        else:
            if is_horizontal(direction):
                direction_vector += direction.value
                break

    hero.set_action('walking', [direction_vector, switch_mode])


def event(hero: Hero):
    switch_mode = pygame.key.get_pressed()[pygame.K_LSHIFT]

    handle_movement(hero, switch_mode)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYUP:
            # movement
            if event.key == pygame.K_a:
                remove_all_directions(hero.movement_queue, Direction.LEFT)
            if event.key == pygame.K_w:
                remove_all_directions(hero.movement_queue, Direction.UP)
            if event.key == pygame.K_d:
                remove_all_directions(hero.movement_queue, Direction.RIGHT)
            if event.key == pygame.K_s:
                remove_all_directions(hero.movement_queue, Direction.DOWN)

        if event.type == pygame.KEYDOWN:
            # movement
            if event.key == pygame.K_a:
                hero.movement_queue.append(Direction.LEFT)
            elif event.key == pygame.K_w:
                hero.movement_queue.append(Direction.UP)
            elif event.key == pygame.K_d:
                hero.movement_queue.append(Direction.RIGHT)
            elif event.key == pygame.K_s:
                hero.movement_queue.append(Direction.DOWN)

            # inventory
            if hero.context == Context.INVENTORY:
                if event.key == pygame.K_UP:
                    hero.inventory.change_focus_item(-1 * game_logic.INVENTORY_COLUMNS_COUNT)
                elif event.key == pygame.K_DOWN:
                    hero.inventory.change_focus_item(game_logic.INVENTORY_COLUMNS_COUNT)
                elif event.key == pygame.K_LEFT:
                    hero.inventory.change_focus_item(-1)
                elif event.key == pygame.K_RIGHT:
                    if (hero.looting_object is not None) & (
                            ((hero.inventory.focus_item_index + 1) % game_logic.INVENTORY_COLUMNS_COUNT == 0) |
                            (hero.inventory.focus_item_index + 1 >= len(hero.inventory.container))):
                        hero.change_context(Context.LOOTING)
                    else:
                        hero.inventory.change_focus_item(1)
                elif event.key == pygame.K_RETURN:
                    focus_item = hero.inventory.get_focus_item()
                    if focus_item:
                        if hero.looting_object and hero.looting_object.inventory.is_open:
                            if isinstance(focus_item, Weapon) and focus_item.is_equipped:
                                continue
                            count = focus_item.count if switch_mode else 1
                            if isinstance(hero.looting_object, Trader):
                                if focus_item.name == 'coin':
                                    continue
                                hero.inventory.add_item(game_logic.get_item('coin'), count * focus_item.cost)
                            hero.inventory.remove_item(focus_item, count)
                            hero.looting_object.inventory.add_item(game_logic.get_item(focus_item.name), count)
                        else:
                            hero.use(focus_item)
                elif game_logic.NUMBER_KEYS.get(event.key) is not None:
                    hero.inventory.set_panel_index(hero.inventory.get_focus_item(),
                                                   game_logic.NUMBER_KEYS.get(event.key) + 1)

            elif hero.context == Context.LOOTING:
                if event.key == pygame.K_UP:
                    hero.looting_object.inventory.change_focus_item(-1 * game_logic.INVENTORY_COLUMNS_COUNT)
                elif event.key == pygame.K_DOWN:
                    hero.looting_object.inventory.change_focus_item(game_logic.INVENTORY_COLUMNS_COUNT)
                elif event.key == pygame.K_LEFT:
                    if hero.inventory.is_open and (
                            hero.looting_object.inventory.focus_item_index % game_logic.INVENTORY_COLUMNS_COUNT == 0):
                        hero.change_context(Context.INVENTORY)
                    else:
                        hero.looting_object.inventory.change_focus_item(-1)
                elif event.key == pygame.K_RIGHT:
                    hero.looting_object.inventory.change_focus_item(1)
                elif event.key == pygame.K_RETURN:
                    looted_item = hero.looting_object.inventory.get_focus_item()
                    if looted_item:
                        count = looted_item.count if switch_mode else 1
                        if isinstance(hero.looting_object, Trader):
                            gold = count * looted_item.cost
                            if gold > hero.get_coins_count():
                                continue
                            hero.inventory.remove_item(game_logic.get_item('coin'), gold)
                        hero.looting_object.inventory.remove_item(looted_item, count)
                        hero.inventory.add_item(game_logic.get_item(looted_item.name), count)
            elif hero.context == Context.GAME:
                if game_logic.NUMBER_KEYS.get(event.key) is not None:
                    item = hero.inventory.inventory_panel[game_logic.NUMBER_KEYS.get(event.key)]
                    if item:
                        hero.use(item)
            elif hero.context == Context.SKILLS:
                if event.key == pygame.K_UP:
                    game_data.skills_panel.current_attribute = max(game_data.skills_panel.current_attribute - 1, 1)
                elif event.key == pygame.K_DOWN:
                    game_data.skills_panel.current_attribute = min(game_data.skills_panel.current_attribute + 1,
                                                                   len(game_data.skills_panel.new_attributes) - 1)
                elif event.key == pygame.K_LEFT:
                    game_data.skills_panel.decrease()
                elif event.key == pygame.K_RIGHT:
                    game_data.skills_panel.increase()
                elif event.key == pygame.K_RETURN:
                    game_data.skills_panel.save()
            elif hero.context == Context.MENU or hero.context == Context.START:
                if event.key == pygame.K_UP:
                    game_data.menu.current_button = max(game_data.menu.current_button - 1, 0)
                elif event.key == pygame.K_DOWN:
                    game_data.menu.current_button = min(game_data.menu.current_button + 1,
                                                        len(game_data.menu.buttons) - 1)
                elif event.key == pygame.K_RETURN:
                    game_data.menu.do_action()
            elif hero.context == Context.DEATH:
                if event.key == pygame.K_RETURN:
                    hero.change_context(Context.START)
                    game_data.menu.show = True

            # other
            if event.key == pygame.K_c:
                if hero.context == Context.MENU or hero.context == Context.START or hero.context == Context.DEATH:
                    continue
                if game_data.skills_panel.show:
                    game_data.skills_panel.close()
                    hero.change_context(Context.GAME)
                else:
                    game_data.skills_panel.open()
                    hero.change_context(Context.SKILLS)
            elif event.key == pygame.K_ESCAPE:
                if game_data.hero.context == Context.START or hero.context == Context.DEATH:
                    return
                game_data.menu.show = not game_data.menu.show
                if game_data.menu.show:
                    game_data.hero.change_context(Context.MENU)
                else:
                    game_data.hero.change_context(Context.GAME)
            elif event.key == pygame.K_SPACE:
                hero.set_action('attacking', None)
            elif event.key == pygame.K_f:
                print(hero.context)
            elif event.key == pygame.K_e:
                hero.interact()
            elif event.key == pygame.K_TAB:
                if hero.context == Context.MENU or hero.context == Context.START or hero.context == Context.DEATH:
                    continue
                if hero.inventory.is_open:
                    if (hero.looting_object is not None) and hero.looting_object.inventory.is_open:
                        hero.change_context(Context.LOOTING)
                        hero.inventory.close()
                    else:
                        hero.change_context(Context.GAME)
                    hero.sounds.get('CloseInv').play(0)
                else:
                    hero.change_context(Context.INVENTORY)
                    hero.sounds.get('OpenInv').play(0)
            elif event.key == pygame.K_F5:
                if hero.context == Context.MENU or hero.context == Context.START or hero.context == Context.DEATH:
                    continue
                save('quicksave')
            elif event.key == pygame.K_F9:
                if hero.context == Context.MENU or hero.context == Context.START or hero.context == Context.DEATH:
                    continue
                load('quicksave')


def run():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Game")

    clock = pygame.time.Clock()

    game_data.init()

    screen = pygame.display.set_mode((game_logic.SCREEN_WIDTH, game_logic.SCREEN_HEIGHT))

    menu_bg = pygame.image.load("res/images/interface/menu/background.png")

    game_data.hero.change_context(Context.START)

    death_message = interface.DeathMessage()

    while True:
        event(game_data.hero)
        if game_data.menu.show:
            screen.blit(menu_bg, (0, 0))
            game_data.menu.draw(screen)
        elif game_data.hero.context == Context.DEATH:
            death_message.draw(screen)
        else:
            clock.tick(game_logic.FPS)
            game_data.update()
            game_data.draw(screen)
        pygame.display.update()
