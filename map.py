import pygame
from item import Item


def location_1(screen):
    bg = pygame.image.load("data/image/bg.png")
    screen.blit(bg, (0, 0))
    coordinates = open("data/FirstLocation.txt", "r").readlines()
    item = Item(screen)
    i = 0
    if str(coordinates[i].rstrip("\n")) == "RockPosition":
        i += 1
        while str(coordinates[i].rstrip("\n")) != "." and str(coordinates[i - 1].rstrip("\n")) != ".":
            item.rock_output(int(coordinates[i]), int(coordinates[i + 1]))
            i += 2
        i += 1
    if str(coordinates[i].rstrip("\n")) == "TreePosition":
        i += 1
        while str(coordinates[i].rstrip("\n")) != "." and str(coordinates[i - 1].rstrip("\n")) != ".":
            item.tree_output(int(coordinates[i]), int(coordinates[i + 1]))
            i += 2
        i += 1

