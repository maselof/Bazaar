from game_object import *
from effect import *
from image_wrapper import *


class Item(GameObject):
    effects: [Effect]
    icon: ImageWrapper
    count: int
    cost: int
    description: str
    bottom_panel_index: int

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
        self.count = 1
        self.cost = cost
        self.description = description
        self.icons_init(animations_path)
        self.bottom_panel_index = 0

    def sounds_init(self):
        pass
        self.sounds = {}
        #self.sounds = {'Use': SoundWrapper(f'res/sounds/objects/{self.name}/use.mp3')}

    def icons_init(self, icons_path: str):
        self.icon = ImageWrapper('res/images/icons/' + icons_path + self.name + '.png')


