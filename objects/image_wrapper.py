import pygame
from pygame import Vector2
from pygame import Surface
from pygame import Rect
from pygame import image
from pygame import transform


class ImageWrapper:
    image: Surface
    rect: Rect
    path: str
    size: Vector2

    def __init__(self,
                 path: str = None,
                 size: Vector2 = None):
        self.path = path
        self.image = image.load(path) if path else Surface([size.x, size.y], pygame.SRCALPHA)
        self.size = size if size else Vector2(self.image.get_size())
        self.rect = Rect(0, 0, self.size.x, self.size.y)

    def set_position(self, point: Vector2):
        self.rect.x, self.rect.y = point

    def get_position(self) -> Vector2:
        return Vector2(self.rect.x, self.rect.y)

    def move(self, vector: Vector2):
        self.rect.x += vector.x
        self.rect.y += vector.y

    def scale(self, scaling_x: float, scaling_y: float):
        width, height = self.image.get_size()
        self.image = transform.scale(self.image, [int(width * scaling_x), int(height * scaling_y)])

    def get_size(self) -> Vector2:
        return Vector2(self.image.get_size())

    def set_size(self, size: Vector2):
        self.image = transform.scale(self.image, [int(size.x), int(size.y)])

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)

    def __getstate__(self):
        return self.path, self.size, self.rect

    def __setstate__(self, state):
        self.path, self.size, self.rect = state
        self.image = image.load(self.path) if self.path else Surface([self.size.x, self.size.y], pygame.SRCALPHA)
        self.size = self.size if self.size else Vector2(self.image.get_size())
