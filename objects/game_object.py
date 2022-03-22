from action import *
from animation import *
from idrawable import *


class GameObject(IDrawable):
    animations_path: str
    name: str
    scaling: float
    image: pygame.image
    rect: pygame.rect.Rect
    collision_rect: pygame.rect.Rect
    size: pygame.Vector2
    collision_rect_offset: pygame.Vector2
    actions: {Action}
    current_action: Action
    direction: Direction
    directional: bool

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
        self.image = self.current_action.animation.get_current_frame(self.direction)

        self.rect = self.image.get_rect()
        self.collision_rect_offset = collision_rect_offset
        col_pos = pygame.Vector2(self.rect.x, self.rect.y) + collision_rect_offset
        self.collision_rect = pygame.Rect(col_pos.x, col_pos.y, size.x, size.y)

    def animations_init(self):
        path = 'res/animations/objects/' + self.animations_path + self.name + '/'
        self.actions = {'idle': Action(self.action_idle, Animation(path, 'idle', self.directional))}
        self.current_action = self.actions['idle']

    def set_position(self, point: pygame.Vector2):
        self.rect.x, self.rect.y = point
        col_pos = pygame.Vector2(self.rect.x, self.rect.y) + self.collision_rect_offset
        self.collision_rect.x, self.collision_rect.y = col_pos

    def get_position(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.x, self.rect.y)

    def get_center(self) -> pygame.Vector2:
        return Vector2(self.rect.center)

    def move(self, vector: pygame.Vector2):
        self.rect.x += vector.x
        self.rect.y += vector.y
        self.collision_rect.x += vector.x
        self.collision_rect.y += vector.y

    def set_action(self, key: str, args: [object]):
        if self.current_action.animation.finished | self.current_action.animation.interruptible:
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
        self.current_action.animation.update(self.direction)

        self.image = self.current_action.animation.get_current_frame(self.direction)
        self.image = pygame.transform.scale(self.image, self.scale_image(self.image.get_size(), self.scaling))

        self.current_action.do()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (0, 255, 0), self.collision_rect)






