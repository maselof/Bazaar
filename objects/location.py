from idrawable import IDrawable
from game_object import *
from entity import *
from interface import HealthBar


class Location(IDrawable):
    objects: [GameObject]
    entities: [str]
    position: Vector2
    size: Vector2

    def __init__(self,
                 objects: [GameObject],
                 entities: [Entity],
                 position: Vector2,
                 size: Vector2):
        self.objects = objects
        self.entities = entities
        self.position = position
        self.size = size

    def set_position(self, position: Vector2):
        self.position = position
        for go in self.objects:
            go.move(position)

    def get_position(self):
        return self.position

    def spawn_entities(self) -> [Entity]:
        entities = []
        for id in self.entities:
            entity = game_logic.get_entity(id)
            hp_bar = HealthBar(entity)
            game_cycle.add_interface_element(hp_bar)
            entities.append(entity)
        return entities

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass