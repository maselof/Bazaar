from objects.point import *
import pygame


class GameObject:
    _position: Point
    name: str
    image: pygame.image
    rect: pygame.rect.Rect

    def __init__(self,
                 position: Point = Point(0, 0),
                 name: str = '',
                 image: pygame.Surface = pygame.Surface([0, 0])):
        self._position = position
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()

    def set_position(self, point: Point):
        self.rect.x, self.rect.y = point.to_array()
        self._position = Point(self.rect.x, self.rect.y)

    def get_position(self) -> Point:
        return self._position






