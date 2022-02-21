import sys

import pygame

from objects.hero import *
from objects.map import *
from interfaces import interface


def draw(object: GameObject, screen: pygame.surface.Surface):
    screen.blit(object.image, object.rect)


def event(screen, hero: Hero):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            sys.exit()

        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_a):
                hero.set_direction(Direction.LEFT)
            if (event.key == pygame.K_w):
                hero.set_direction(Direction.UP)
            if (event.key == pygame.K_d):
                hero.set_direction(Direction.RIGHT)
            if (event.key == pygame.K_s):
                hero.set_direction(Direction.DOWN)
            if (event.key == pygame.K_ESCAPE):
                interface.pause(screen)


def run():
    pygame.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((1680, 1080))
    clock = pygame.time.Clock()

    hero = Hero()
    hero.set_position(Point(100, 100))
    map = Map()

    while True:
        clock.tick(60)
        game_logic.g_timer = (game_logic.g_timer + 1) % 60
        hero.update()
        event(screen, hero)
        draw(map, screen)
        draw(hero, screen)
        pygame.display.update()
