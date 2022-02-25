import pygame.image

from entity import *


class Hero(Entity):
    def __init__(self,
                 scaling: float = 1):
        super().__init__('hero', '', scaling)


