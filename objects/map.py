from objects.game_object import *


class Map(GameObject):
    def __init__(self):
        super().__init__()
        self.name = 'Map'
        self.image = pygame.image.load('res/image/bg.png')
        self.rect = self.image.get_rect()