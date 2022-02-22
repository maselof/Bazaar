import pygame.image

from entity import *


class Hero(Entity):
    def __init__(self):
        super().__init__()
        self.animations = [pygame.image.load('res/image/LEFT1.png'), pygame.image.load('res/image/LEFT2.png'),
                           pygame.image.load('res/image/UP1.png'), pygame.image.load('res/image/UP2.png'),
                           pygame.image.load('res/image/RIGHT1.png'), pygame.image.load('res/image/RIGHT2.png'),
                           pygame.image.load('res/image/DOWN1.png'), pygame.image.load('res/image/DOWN2.png')]

