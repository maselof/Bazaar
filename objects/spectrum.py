import pygame

from idrawable import IDrawable
from image_wrapper import ImageWrapper


class Spectrum(IDrawable):
    surface: ImageWrapper
    color: pygame.Color
    speed: float
    border: int
    finished: bool
    __counter: int

    def __init__(self,
                 size: pygame.Vector2,
                 position: pygame.Vector2,
                 color: pygame.Color,
                 speed: float,
                 border: int):
        self.surface = ImageWrapper(size=size)
        self.surface.set_size(size)
        self.surface.set_position(position)
        self.size = size
        self.color = color
        self.surface.image.fill((color.r, color.g, color.b, 0))
        self.speed = speed
        self.border = border
        self.finished = True

    def start(self):
        self.finished = False
        self.surface.image.fill((self.color.r, self.color.g, self.color.b, 0))
        self.__counter = 0

    def update(self):
        if self.finished:
            return

        self.__counter = min(int(self.__counter + self.speed), self.border)
        self.surface.image.fill((self.color.r, self.color.g, self.color.b, self.__counter))
        if self.__counter >= self.border:
            self.finished = True

    def draw(self, screen: pygame.Surface):
        self.surface.draw(screen)
