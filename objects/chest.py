from game_object import *
from inventory import ILootable, GameContainer


class Chest(GameObject, ILootable):

    is_open: bool

    def __init__(self,
                 name: str,
                 animations_path: str,
                 size: Vector2,
                 collision_rect_offset: Vector2):
        super().__init__(name, animations_path, size, collision_rect_offset, False, 1)
        self.inventory = GameContainer()
        self.is_open = False

    def animations_init(self):
        path = 'res/animations/objects/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle', self.directional)),
                        'open': Action(self.action_open, Animation(path, 'open', self.directional))}
        self.current_action = self.actions['idle']

    def action_open(self, args: [object]):
        pass

    def open(self):
        self.is_open = True
        self.inventory.open()
        self.set_action('open', None)

    def close(self):
        self.is_open = False
        self.inventory.close()
        self.set_action('idle', None)
