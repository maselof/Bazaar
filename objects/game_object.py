import pygame
from pygame import Vector2

from action import Action
from animation import Animation
from idrawable import IDrawable
from sound_wrapper import SoundWrapper
from image_wrapper import ImageWrapper
from direction import Direction


class GameObject(IDrawable):
    animations_path: str
    name: str
    scaling: float
    image: ImageWrapper
    collision_rect: pygame.rect.Rect
    size: pygame.Vector2
    collision_rect_offset: pygame.Vector2
    actions: {Action}
    current_action: Action
    direction: Direction
    directional: bool
    sounds: {str: SoundWrapper}

    def __init__(self,
                 name: str,
                 animations_path: str,
                 size: pygame.Vector2,
                 collision_rect_offset: pygame.Vector2 = Vector2(0, 0),
                 directional: bool = True,
                 scaling: float = 1,
                 ):
        self.name = name
        self.animations_path = animations_path
        self.directional = directional
        self.scaling = scaling
        self.size = size

        self.animations_init()
        self.direction = Direction.LEFT if directional else Direction.STAND
        self.image = ImageWrapper(size=size)
        self.image.image = self.current_action.animation.get_current_frame(self.direction)

        self.collision_rect_offset = collision_rect_offset
        col_pos = pygame.Vector2(self.image.rect.x, self.image.rect.y) + collision_rect_offset
        self.collision_rect = pygame.Rect(col_pos.x, col_pos.y, size.x, size.y)
        self.sounds_init()
        self.scale_sounds(0)

    def animations_init(self):
        path = 'res/animations/objects/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle', self.directional))}
        self.current_action = self.actions['idle']

    def sounds_init(self):
        self.sounds = {'Idle': SoundWrapper(None)}

    def scale_sounds(self, scaling: float):
        for sound in self.sounds.values():
            sound.set_volume(sound.volume * scaling)

    def set_position(self, point: pygame.Vector2):
        self.image.rect.x, self.image.rect.y = point
        col_pos = pygame.Vector2(self.image.rect.x, self.image.rect.y) + self.collision_rect_offset
        self.collision_rect.x, self.collision_rect.y = col_pos

    def get_position(self) -> pygame.Vector2:
        return pygame.Vector2(self.image.rect.x, self.image.rect.y)

    def get_center(self) -> pygame.Vector2:
        return Vector2(self.image.rect.center)

    def move(self, vector: pygame.Vector2):
        self.image.rect.x += vector.x
        self.image.rect.y += vector.y
        self.collision_rect.x += vector.x
        self.collision_rect.y += vector.y

    def set_action(self, key: str, args: [object]):
        if self.current_action.animation.finished | self.current_action.animation.interruptable:
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

        self.image.image = self.current_action.animation.get_current_frame(self.direction)
        self.image.image = pygame.transform.scale(self.image.image, self.scale_image(self.image.get_size(),
                                                                                     self.scaling))

        self.current_action.do()

    def draw(self, screen: pygame.Surface):
        self.image.draw(screen)
