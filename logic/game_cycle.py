import sys
from hero import *
from map import *
import interface
import game_logic
from pygame.math import Vector2


def draw(object, screen: pygame.surface.Surface):
    screen.blit(object.image, object.rect)


def handle_movement(hero):

    directions = [Direction.STAND, Direction.STAND]
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_a]:
        directions[0] = Direction.LEFT
    elif pressed_keys[pygame.K_d]:
        directions[0] = Direction.RIGHT

    if pressed_keys[pygame.K_w]:
        directions[1] = Direction.UP
    elif pressed_keys[pygame.K_s]:
        directions[1] = Direction.DOWN

    if directions == [Direction.STAND, Direction.STAND]:
        hero.set_action('idle', None)
    else:
        hero.set_action('walking', directions)


def event(screen, hero: Hero):

    handle_movement(hero)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
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
    screen = pygame.display.set_mode((1680, 1050))
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
    screen = pygame.display.set_mode((1680, 1080))
    clock = pygame.time.Clock()

    hero = Hero(0.5)
    hero.set_position(Vector2(100, 100))

    hb = interface.HealthBar(hero)

    potion = GameObject('heal_potion', 'potions/', 1)
    potion.set_position(Vector2(100, 100))

    map = Map()

    while True:
        clock.tick(game_logic.g_fps)
        game_logic.g_timer = (game_logic.g_timer + 1) % game_logic.g_fps
        hero.update()
        potion.update()
        hb.update()
        event(screen, hero)
        draw(map, screen)
        draw(hero, screen)
        draw(potion, screen)
        hb.draw(screen)
        pygame.display.update()