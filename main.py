import pygame
import sys

import control
from hero import Hero
import map


def run():
    pygame.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((1680, 1080))
    hero = Hero(screen)
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        map.location_1(screen)
        control.event(hero)
        hero.update_hero(screen)
        hero.output()
        pygame.display.update()


run()
