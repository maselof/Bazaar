from game_object import *


class Weapon(GameObject):

    def __init__(self,
                 name: str):
        super().__init__(name, 'weapons/', True)

    def animations_init(self):
        path = 'res/animations/objects/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle')),
                        'walking': Action(self.action_idle, Animation(path, 'walking')),
                        'attacking': Action(self.action_idle, Animation(path, 'attacking'))}
        self.current_action = self.actions['idle']
