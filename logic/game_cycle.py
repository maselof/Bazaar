import sys
from map import *
import interface
from camera import *


def draw(object, screen: pygame.surface.Surface):
    screen.blit(object.image, object.rect)


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


def run():
    pygame.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((game_logic.g_screen_width, game_logic.g_screen_height))
    clock = pygame.time.Clock()

    hero = Hero(1)
    cudgel = Weapon('cudgel')
    hero.set_weapon(cudgel)

    hero.update()
    hero_width, hero_height = hero.image.get_size()
    center = Vector2((game_logic.g_screen_width - hero_width) // 2,
                     (game_logic.g_screen_height - hero_height) // 2)
    print(hero_width, hero_height, center)
    hero.set_position(center)

    hb = interface.HealthBar(hero)

    potion = GameObject('heal_potion', 'potions/', False, 1)
    potion.set_position(Vector2(100, 100))

    map = Map()
    map.game_objects.append(potion)

    camera = Camera(map, hero)

    while True:
        clock.tick(game_logic.g_fps)
        game_logic.g_timer = (game_logic.g_timer + 1) % game_logic.g_fps
        potion.update()
        hb.update()
        hero.update()
        cudgel.update()
        camera.update()
        event(screen, hero)
        draw(map, screen)
        draw(potion, screen)
        hb.draw(screen)
        draw(hero, screen)
        draw(cudgel, screen)
        pygame.display.update()
