from game_object import *


class Map:
    image: pygame.Surface
    rect: pygame.Rect
    game_objects: [GameObject]

    def __init__(self):
        self.image = pygame.image.load('res/images/bg.png')
        self.rect = self.image.get_rect()
        self.game_objects = []

    def move(self, vector: pygame.Vector2):
        self.rect.x += vector.x
        self.rect.y += vector.y
