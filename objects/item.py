from game_object import *
from effect import *
from image_wrapper import *


class Item(GameObject):
    effects: [Effect]
    icon: ImageWrapper
    count: int

    def __init__(self,
                 name: str,
                 animations_path: str,
                 size: Vector2,
                 directional: bool,
                 scaling: float,
                 effects: [Effect]):
        super().__init__(name, animations_path, size, directional, scaling)
        self.effects = effects
        self.icon = ImageWrapper('res/images/icons/' + self.name + '.png')
        self.count = 1


