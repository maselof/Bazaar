from pygame import Vector2

import item
from action import Action
from animation import Animation
from item import Item
from effect import Effect
from image_wrapper import ImageWrapper


class Weapon(Item):
    attack_range: float
    attack_effects: [Effect]

    is_equipped: bool
    equipped_icon: ImageWrapper
    not_equipped_icon: ImageWrapper

    def __init__(self,
                 name: str,
                 attack_range: float,
                 hero_effects: [Effect],
                 attack_effects: [Effect],
                 cost: int,
                 description: str):
        super().__init__(name, 'weapons/', Vector2(0, 0), True, 1, hero_effects, cost, description)
        self.attack_range = attack_range
        self.attack_effects = attack_effects

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

    def icons_init(self, icons_path: str):
        self.not_equipped_icon = ImageWrapper('res/images/icons/weapons/' + self.name + '/1.png')
        self.equipped_icon = ImageWrapper('res/images/icons/weapons/' + self.name + '/2.png')
        self.icon = self.not_equipped_icon

