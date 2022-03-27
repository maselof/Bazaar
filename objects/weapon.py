from pygame import Vector2

from action import Action
from animation import Animation
from item import Item
from effect import Effect
from image_wrapper import ImageWrapper
from sound_wrapper import SoundWrapper


class Weapon(Item):
    attack_range: float
    attack_effects: [Effect]

    is_equipped: bool
    equipped_icon: ImageWrapper
    not_equipped_icon: ImageWrapper

    damage: int
    attack_speed_modifier: float

    def __init__(self,
                 name: str,
                 damage: int,
                 attack_speed_modifier: float,
                 attack_range: float,
                 hero_effects: [Effect],
                 attack_effects: [Effect],
                 cost: int,
                 description: str,
                 trading_count: int):
        super().__init__(name, 'weapons/', Vector2(0, 0), True, 1, hero_effects, cost, description, trading_count)
        self.attack_range = attack_range
        self.attack_effects = attack_effects
        self.damage = damage
        self.attack_speed_modifier = attack_speed_modifier

        self.set_equipped(False)

    def set_equipped(self, equipped: bool):
        self.is_equipped = equipped
        self.icon = self.equipped_icon if equipped else self.not_equipped_icon

    def animations_init(self):
        path = 'res/animations/objects/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle')),
                        'walking': Action(self.action_idle, Animation(path, 'walking')),
                        'attacking': Action(self.action_idle, Animation(path, 'attacking'))}
        self.current_action = self.actions['idle']

    def sounds_init(self):
        self.sounds = {'Slash': SoundWrapper(f'res/sounds/weapons/{self.name}/slash.mp3', True, 1),
                       'Damage': SoundWrapper(f'res/sounds/weapons/{self.name}/damage.mp3', True, 1)}

    def icons_init(self, icons_path: str):
        self.not_equipped_icon = ImageWrapper('res/images/icons/weapons/' + self.name + '/1.png')
        self.equipped_icon = ImageWrapper('res/images/icons/weapons/' + self.name + '/2.png')
        self.icon = self.not_equipped_icon
