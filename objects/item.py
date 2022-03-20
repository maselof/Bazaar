from game_object import *
from effect import *
from image_wrapper import *


class Item(GameObject):
    effects: [Effect]
    icon: ImageWrapper
    count: int
    cost: int
    description: str

    def __init__(self,
                 name: str,
                 animations_path: str,
                 size: Vector2,
                 directional: bool,
                 scaling: float,
                 effects: [Effect],
                 cost: int,
                 description: str):
        super().__init__(name, animations_path, size, Vector2(0, 0), directional, scaling)
        self.effects = effects
        self.icon = ImageWrapper('res/images/icons/' + self.name + '.png')
        self.count = 1
        self.cost = cost
        self.description = description


