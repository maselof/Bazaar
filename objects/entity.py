import game_logic
from game_object import *
from action import *
from pygame.math import Vector2
from weapon import Weapon


class Entity(GameObject):
    speed: int
    direction_vector: Vector2
    left_flip: bool

    max_hp: int
    hp: int

    weapon: Weapon

    def __init__(self,
                 name: str,
                 animations_path: str,
                 size: Vector2,
                 scaling: float = 1
                 ):
        super().__init__(name, animations_path, size, True, scaling)

        self.speed = 5
        self.direction_vector = Vector2(0, 0)
        self.left_flip = False
        self.direction = Direction.LEFT

        self.max_hp = 100
        self.hp = 100

        self.weapon = Weapon('fists', Vector2(0, 0))

    def animations_init(self):
        path = 'res/animations/entities/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle', True)),
                        'walking': Action(self.action_walking, Animation(path, 'walking', True, True, game_logic.g_entity_walking_anim_speed)),
                        'attacking': Action(self.action_attacking, Animation(path, 'attacking', True, False, game_logic.g_entity_attacking_anim_speed))}
        self.current_action = self.actions['idle']

    def set_position(self, point: pygame.Vector2):
        super().set_position(point)
        self.weapon.set_position(point)

    def move(self, vector: pygame.Vector2):
        super().move(vector)
        self.weapon.move(vector)

    def action_idle(self, args: [object]):
        super().action_idle(args)

        self.direction_vector = Direction.STAND.value

    def action_walking(self, args: [object]):
        self.direction_vector = args[0]
        new_pos = self.get_position() + self.direction_vector * self.speed
        self.set_position(new_pos)

    def action_attacking(self, args: [object]):
        pass

    def set_weapon(self, weapon: Weapon):
        self.weapon = weapon

        self.weapon.actions.get('walking').animation.speed = self.actions.get('walking').animation.speed
        self.weapon.actions.get('attacking').animation.speed = self.actions.get('attacking').animation.speed

    def update(self):
        super().update()
        self.weapon.set_position(self.get_position())
        self.weapon.direction = self.direction
        self.weapon.set_action(self.current_action.animation.name, self.current_action.args)
        self.weapon.update()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        self.weapon.draw(screen)

