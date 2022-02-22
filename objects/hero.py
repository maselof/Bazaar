import pygame.image

from entity import *


class Hero(Entity):
    def __init__(self):
        super().__init__()
        self.animations = [pygame.image.load('res/images/1.png'), pygame.image.load('res/images/2.png'),
                           pygame.image.load('res/images/1.png'), pygame.image.load('res/images/2.png'),
                           pygame.image.load('res/images/1.png'), pygame.image.load('res/images/2.png'),
                           pygame.image.load('res/images/1.png'), pygame.image.load('res/images/2.png')]

