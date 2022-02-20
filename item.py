import pygame


class Item:
    def __init__(self, screen):
        self.image_rock = pygame.image.load("data/image/rock_1.png")
        self.image_tree = pygame.image.load("data/image/tree.png")
        self.screen = screen

    def rock_output(self, x, y):
        self.screen.blit(self.image_rock, (x, y))

    def tree_output(self, x, y):
        self.screen.blit(self.image_tree, (x, y))

