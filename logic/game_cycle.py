import sys
import pygame
from map import *
import interface
from camera import *
from inventory import HeroInventory
from copy import copy
from chest import Chest


def remove_all_directions(queue: [Direction], direction: Direction):
    for i in range(queue.count(direction)):
        queue.remove(direction)


def draw(screen: pygame.Surface, image: pygame.Surface, rect: pygame.Surface):
    screen.blit(image, rect)


def handle_movement(hero):

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

    for dir in reversed_queue:
        if is_horizontal(priority_direction):
            if not is_horizontal(dir):
                direction_vector += dir.value
                break
        else:
            if is_horizontal(dir):
                direction_vector += dir.value
                break

    hero.set_action('walking', direction_vector)


def event(screen, hero: Hero):
    handle_movement(hero)
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
                    hero.inventory.change_focus_item(-1 * game_logic.inventory_columns_count)
                elif event.key == pygame.K_DOWN:
                    hero.inventory.change_focus_item(game_logic.inventory_columns_count)
                elif event.key == pygame.K_LEFT:
                    hero.inventory.change_focus_item(-1)
                elif event.key == pygame.K_RIGHT:
                    if (hero.looting_object != None) & (
                            ((hero.inventory.focus_item_index + 1) % game_logic.inventory_columns_count == 0) |
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
                            hero.inventory.remove_item(focus_item)
                            print('GIVE ' + focus_item.name)
                            hero.looting_object.inventory.add_item(game_logic.get_item(focus_item.name))
                        else:
                            hero.use(focus_item)
                elif game_logic.NUMBER_KEYS.get(event.key) is not None:
                    hero.inventory.set_panel_index(hero.inventory.get_focus_item(), game_logic.NUMBER_KEYS.get(event.key) + 1)

            elif hero.context == Context.LOOTING:
                if event.key == pygame.K_UP:
                    hero.looting_object.inventory.change_focus_item(-1 * game_logic.inventory_columns_count)
                elif event.key == pygame.K_DOWN:
                    hero.looting_object.inventory.change_focus_item(game_logic.inventory_columns_count)
                elif event.key == pygame.K_LEFT:
                    if (hero.inventory.is_open) & ((hero.looting_object.inventory.focus_item_index % game_logic.inventory_columns_count == 0)):
                        hero.change_context(Context.INVENTORY)
                    else:
                        hero.looting_object.inventory.change_focus_item(-1)
                elif event.key == pygame.K_RIGHT:
                    hero.looting_object.inventory.change_focus_item(1)
                elif event.key == pygame.K_RETURN:
                    looted_item = hero.looting_object.inventory.get_focus_item()
                    if looted_item:
                        hero.looting_object.inventory.remove_item(looted_item)
                        print('GET ' + looted_item.name)
                        hero.inventory.add_item(game_logic.get_item(looted_item.name))
            elif hero.context == Context.GAME:
                if game_logic.NUMBER_KEYS.get(event.key) is not None:
                    item = hero.inventory.inventory_panel[game_logic.NUMBER_KEYS.get(event.key)]
                    if item:
                        hero.use(item)

            # other
            if event.key == pygame.K_r:
                print(hero.movement_queue)
            elif event.key == pygame.K_ESCAPE:
                interface.pause(screen)
            elif event.key == pygame.K_SPACE:
                hero.set_action('attacking', None)
            elif event.key == pygame.K_f:
                hero.stats.hp -= 10
            elif event.key == pygame.K_e:
                hero.interact()
            elif event.key == pygame.K_TAB:
                if hero.inventory.is_open:
                    if (hero.looting_object != None) and hero.looting_object.inventory.is_open:
                        hero.change_context(Context.LOOTING)
                        hero.inventory.close()
                    else:
                        hero.change_context(Context.GAME)
                else:
                    hero.change_context(Context.INVENTORY)


def show_menu():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((game_logic.g_screen_width, game_logic.g_screen_height))
    menu_bg = pygame.image.load("res/images/interface/menu/background.png")
    show = True
    start_button = interface.Button(540, 100, screen)
    quit_button = interface.Button(540, 100, screen)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bg, (0, 0))
        start_button.draw(screen.get_size()[0] // 2 - 250, screen.get_size()[1] // 2 - 150, "Start Game", run, 70)
        quit_button.draw(screen.get_size()[0] // 2 - 250, screen.get_size()[1] // 2, "Quit", pygame.quit, 70)
        pygame.display.update()


def add_entity(entity: Entity, game_map: Map, game_interface: interface.Interface):
    game_interface.elements.append(interface.HealthBar(entity))
    game_map.add_game_object(entity)


def add_game_object(game_object: GameObject, game_map: Map):
    game_map.add_game_object(game_object)


def add_interface_element(element: IDrawable):
    game_interface.elements.append(element)
    game_interface.elements.sort(key=lambda el: el.priority)


game_interface = interface.Interface()
game_map = Map()


def get_collided_visible_objects(game_object: GameObject, area: [pygame.Rect]) -> [GameObject]:
    collided = []
    for go in game_map.visible_game_objects:
        if go == game_object:
            continue

        for r in area:
            if go.collision_rect.colliderect(r):
                collided.append(go)
                break
    return collided


def get_nearest_object(game_object: GameObject) -> [GameObject, float]:
    pos = Vector2(game_object.rect.centerx, game_object.rect.centery)

    min_distance = 1000000
    nearest_object = None
    if game_map.hero != game_object:
        min_distance = pos.distance_to(Vector2(game_map.hero.rect.centerx, game_map.hero.rect.centery))
        nearest_object = game_map.hero

    for go in game_map.visible_game_objects:
        if go == game_object:
            continue

        go_pos = Vector2(go.rect.centerx, go.rect.centery)
        distance = go_pos.distance_to(pos)
        if distance < min_distance:
            min_distance = distance
            nearest_object = go
    return [nearest_object, min_distance]


def get_distance(object1: GameObject, object2: GameObject):
    return object1.get_center().distance_to(object2.get_center())


def check_collisions(game_object: GameObject, vector: Vector2) -> Vector2:
    dir_vector = vector
    offset = Vector2(game_logic.collision_offset * (1 if dir_vector.x > 0 else -1 if dir_vector.x < 0 else 0),
                     game_logic.collision_offset * (1 if dir_vector.y > 0 else -1 if dir_vector.y < 0 else 0))
    collision_rect = game_object.collision_rect.copy()
    for go in game_map.visible_game_objects:
        if go == game_object:
            continue
        if dir_vector == Vector2(0, 0):
            return dir_vector
        if go.collision_rect.colliderect(collision_rect.move(vector.x + offset.x, 0)):
            dir_vector.x = 0
        if go.collision_rect.colliderect(collision_rect.move(0, vector.y + offset.y)):
            dir_vector.y = 0
        if dir_vector == Vector2(1, 1) and go.collision_rect.colliderect(collision_rect.move(vector.x + offset.x, vector.y + offset.y)):
            dir_vector = Vector2(0, 0)
    return dir_vector


def run():
    pygame.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((game_logic.g_screen_width, game_logic.g_screen_height))
    clock = pygame.time.Clock()

    hero = Hero(Vector2(game_logic.g_hero_width, game_logic.g_hero_height), game_logic.entity_collision_offset)
    hero.update()
    hero_width, hero_height = hero.image.get_size()
    center = Vector2((game_logic.g_screen_width - hero_width) // 2,
                     (game_logic.g_screen_height - hero_height) // 2)
    hero.set_position(center)
    add_interface_element(interface.HeroBars(hero))
    add_interface_element(hero.inventory)
    hero_weapon = game_logic.get_item('fists')
    hero.set_weapon(hero_weapon)
    game_map.hero = hero
    add_game_object(hero, game_map)

    potion = game_logic.get_item('heal_potion')
    potion.set_position(Vector2(800, 800))
    add_game_object(potion, game_map)

    cudgel = game_logic.get_item('cudgel')
    cudgel.set_position(Vector2(700, 200))
    add_game_object(cudgel, game_map)

    cudgel = game_logic.get_item('cudgel')
    cudgel.set_position(Vector2(800, 200))
    add_game_object(cudgel, game_map)

    sword = game_logic.get_item('sword')
    sword.set_position(Vector2(750, 200))
    add_game_object(sword, game_map)

    entity = Entity('bandit', '', Vector2(30, 70), game_logic.entity_collision_offset)
    entity.set_position(Vector2(200, 200))
    entity.set_weapon(game_logic.get_item('fists'))
    entity.inventory.add_item(game_logic.get_item('cudgel'))
    entity.inventory.add_item(game_logic.get_item('heal_potion'))
    entity.set_weapon(game_logic.get_item('cudgel'))
    add_entity(entity, game_map, game_interface)
    add_interface_element(entity.inventory)

    chest = Chest('chest', 'general/', Vector2(58, 5), Vector2(1, 25))
    chest.set_position(Vector2(500, 500))
    add_interface_element(chest.inventory)
    add_game_object(chest, game_map)

    camera = Camera(game_map, hero)
    dialog_window = interface.DialogWindow(hero)
    add_interface_element(dialog_window)

    while True:
        clock.tick(game_logic.g_fps)
        game_logic.g_timer = (game_logic.g_timer + 1) % game_logic.g_fps
        pygame.draw.rect(screen, (255, 255, 255), Rect(0, 0, game_logic.g_screen_width, game_logic.g_screen_height))

        game_map.update()
        camera.update()
        game_interface.update()

        event(screen, hero)
        game_map.draw(screen)
        game_interface.draw(screen)

        pygame.display.update()
