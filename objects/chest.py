from pygame import Vector2

from game_object import GameObject
from inventory import ILootable
from inventory import GameContainer
from action import Action
from animation import Animation
from sound_wrapper import SoundWrapper


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

    def sounds_init(self):
        self.sounds = {'Open': SoundWrapper(f'res/sounds/objects/chests/{self.name}/open.mp3', True, 0.1),
                       'Close': SoundWrapper(f'res/sounds/objects/chests/{self.name}/close.mp3', True, 0.1)}

    def action_open(self, args: [object]):
        pass

    def open(self):
        self.is_open = True
        self.inventory.open()
        self.set_action('open', None)
        self.sounds.get('Open').play(0)

    def close(self):
        self.is_open = False
        self.inventory.close()
        self.set_action('idle', None)
        self.sounds.get('Close').play(0)
