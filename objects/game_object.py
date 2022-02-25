import pygame
from pygame import Vector2
from action import *


class GameObject:
    _position: Vector2
    animations_path: str
    name: str
    scaling: float
    image: pygame.image
    rect: pygame.rect.Rect
    actions: {Action}
    current_action: Action

    def __init__(self,
                 name: str = '',
                 animations_path: str = '',
                 scaling: float = 1,
                 position: Vector2 = Vector2(0, 0),
                 ):
        self.animations_path = animations_path
        self.name = name
        self.scaling = scaling
        self._position = position
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()
        self.animations_init()

    def animations_init(self):
        path = 'res/animations/objects/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path + 'Idle'))}
        self.current_action = self.actions['idle']

    def set_position(self, point: Vector2):
        self.rect.x, self.rect.y = point
        self._position = point

    def get_position(self) -> Vector2:
        return self._position

    def set_action(self, key: str, args: [object]):
        self.current_action = self.actions.get(key)
        self.current_action.set_args(args)

    def action_idle(self, args: [object]):
        pass

    def scale_image(self, initial_size: [int], scaling: float) -> [int]:
        width, height = initial_size
        return [int(width * scaling), int(height * scaling)]

    def update(self):
        if self.current_action.animation.finished:
            self.current_action.animation.start()
        self.current_action.animation.update()

        self.image = self.current_action.animation.get_current_frame()
        self.image = pygame.transform.scale(self.image, self.scale_image(self.image.get_size(), self.scaling))

        self.current_action.do()






