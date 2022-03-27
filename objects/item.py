from pygame import Vector2

from game_object import GameObject
from effect import Effect
from image_wrapper import ImageWrapper


class Item(GameObject):
    effects: [Effect]
    icon: ImageWrapper
    count: int
    cost: int
    description: str
    bottom_panel_index: int
    trading_count: int

    def __init__(self,
                 name: str,
                 animations_path: str,
                 size: Vector2,
                 directional: bool,
                 scaling: float,
                 effects: [Effect],
                 cost: int,
                 description: str,
                 trading_count: int):
        super().__init__(name, animations_path, size, Vector2(0, 0), directional, scaling)
        self.effects = effects
        self.count = 1
        self.cost = cost
        self.description = description
        self.icons_init(animations_path)
        self.bottom_panel_index = 0
        self.trading_count = trading_count

    def sounds_init(self):
        self.sounds = {}

    def icons_init(self, icons_path: str):
        self.icon = ImageWrapper('res/images/icons/' + icons_path + self.name + '.png')
