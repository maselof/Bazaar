import pygame
import sys


def event(hero):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            """движение персонажа"""
            if event.key == pygame.K_d:
                hero.mright = True
            elif event.key == pygame.K_a:
                hero.mleft = True
            elif event.key == pygame.K_w:
                hero.mup = True
            elif event.key == pygame.K_s:
                hero.mdown = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                hero.mright = False
            elif event.key == pygame.K_a:
                hero.mleft = False
            elif event.key == pygame.K_w:
                hero.mup = False
            elif event.key == pygame.K_s:
                hero.mdown = False


