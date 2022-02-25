from game_object import *


class Map:
    def __init__(self):
        self.image = pygame.image.load('res/images/bg.png')
        self.rect = self.image.get_rect()