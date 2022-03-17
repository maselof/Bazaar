from pygame import Vector2
from pygame import Surface
from pygame import Rect
from pygame import image
from pygame import transform


class ImageWrapper:
    image: Surface
    rect: Rect

    def __init__(self,
                 path: str = None,
                 surface: Surface = None):
        if path:
            self.image = image.load(path)
        elif surface:
            self.image = surface
        else:
            self.image = Surface(0, 0)

        width, height = self.image.get_size()
        self.rect = Rect(0, 0, width, height)

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
