import pygame


class IDrawable:

    priority: int

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass
