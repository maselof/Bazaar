import sys

import pygame

import game_logic
from entity import Direction
from game_object import *
from hero import *
from map import *
import interface


def draw(object: GameObject, screen: pygame.surface.Surface):
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


def run():
    pygame.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((1680, 1080))
    clock = pygame.time.Clock()

    hero = Hero()
    hero.set_position(Vector2(100, 100))
    map = Map()

    while True:
        clock.tick(game_logic.g_fps)
        game_logic.g_timer = (game_logic.g_timer + 1) % game_logic.g_fps
        hero.update()
        event(screen, hero)
        draw(map, screen)
        draw(hero, screen)
        pygame.display.update()
