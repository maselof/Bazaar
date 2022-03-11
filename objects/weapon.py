from pygame import Vector2
from action import Action
from animation import Animation
from item import Item
from effect import Effect


class Weapon(Item):
    attack_range: float
    attack_effects: [Effect]

    def __init__(self,
                 name: str,
                 attack_range: float,
                 hero_effects: [Effect],
                 attack_effects: [Effect]):
        super().__init__(name, 'weapons/', Vector2(0, 0), True, 1, hero_effects)
        self.attack_range = attack_range
        self.attack_effects = attack_effects

    def animations_init(self):
        path = 'res/animations/objects/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle')),
                        'walking': Action(self.action_idle, Animation(path, 'walking')),
                        'attacking': Action(self.action_idle, Animation(path, 'attacking'))}
        self.current_action = self.actions['idle']

