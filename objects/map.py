from idrawable import *


class Map(IDrawable):
    image: pygame.Surface
    rect: pygame.Rect
    game_objects: [IDrawable]
    hero: IDrawable

    def __init__(self):
        self.image = pygame.image.load('res/images/bg.png')
        self.rect = self.image.get_rect()
        self.game_objects = []

    def move(self, vector: pygame.Vector2):
        self.rect.x += vector.x
        self.rect.y += vector.y

    def update(self):
        for go in self.game_objects:
            go.update()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        for go in self.game_objects:
            go.draw(screen)
