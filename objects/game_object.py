import pygame
from pygame import Vector2


class GameObject:
    _position: Vector2
    name: str
    image: pygame.image
    rect: pygame.rect.Rect

    def __init__(self,
                 position: Vector2 = Vector2(0, 0),
                 name: str = '',
                 image: pygame.Surface = pygame.Surface([0, 0])):
        self._position = position
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()

    def set_position(self, point: Vector2):
        self.rect.x, self.rect.y = point
        self._position = point

    def get_position(self) -> Vector2:
        return self._position






