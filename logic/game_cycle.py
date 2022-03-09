import sys
from map import *
import interface
from camera import *


def is_horizontal(direction: Direction):
    return direction == Direction.LEFT or direction == Direction.RIGHT


def remove_all_directions(queue: [Direction], direction: Direction):
    for i in range(queue.count(direction)):
        queue.remove(direction)


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

            # other
            if event.key == pygame.K_r:
                print(hero.movement_queue)
            if event.key == pygame.K_ESCAPE:
                interface.pause(screen)
            if event.key == pygame.K_SPACE:
                hero.set_action('attacking', None)
            if event.key == pygame.K_f:
                hero.hp -= 10


def show_menu():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((game_logic.g_screen_width, game_logic.g_screen_height))
    menu_bg = pygame.image.load("res/images/bg.png")
    show = True
    start_button = interface.Button(540, 100, screen)
    quit_button = interface.Button(540, 100, screen)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bg, (0, 0))
        start_button.draw(300, 200, "Start Game", run, 70)
        quit_button.draw(300, 400, "Quit", pygame.quit, 70)
        pygame.display.update()


def add_entity(entity: Entity, game_map: Map, game_interface: interface.Interface):
    game_interface.elements.append(interface.HealthBar(entity))
    game_map.game_objects.append(entity)


def add_game_object(game_object: GameObject, game_map: Map, game_interface: interface.Interface):
    game_map.game_objects.append(game_object)


def run():
    pygame.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((game_logic.g_screen_width, game_logic.g_screen_height))
    clock = pygame.time.Clock()

    game_map = Map()
    game_interface = interface.Interface()

    hero = Hero(Vector2(game_logic.g_hero_width, game_logic.g_hero_height))
    hero.update()
    hero_width, hero_height = hero.image.get_size()
    center = Vector2((game_logic.g_screen_width - hero_width) // 2,
                     (game_logic.g_screen_height - hero_height) // 2)
    hero.set_position(center)
    game_interface.elements.append(interface.HealthBar(hero))
    cudgel = Weapon('cudgel', Vector2(0, 0))
    # hero.set_weapon(cudgel)

    potion = GameObject('heal_potion', 'potions/', Vector2(0, 0), False, 1)
    potion.set_position(Vector2(100, 100))
    add_game_object(potion, game_map, game_interface)

    entity = Entity('hero', '', Vector2(30, 70))
    entity.set_position(Vector2(200, 200))
    cudgel2 = Weapon('cudgel', Vector2(0, 0))
    entity.set_weapon(cudgel2)
    add_entity(entity, game_map, game_interface)

    camera = Camera(game_map, hero)

    while True:
        clock.tick(game_logic.g_fps)
        game_logic.g_timer = (game_logic.g_timer + 1) % game_logic.g_fps

        game_map.update()
        hero.update()
        camera.update()
        game_interface.update()

        event(screen, hero)
        game_map.draw(screen)
        hero.draw(screen)
        game_interface.draw(screen)

        pygame.display.update()
