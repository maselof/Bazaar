import random

import pygame
from pygame import Vector2

import game_logic
import game_cycle
from entity import Entity
from game_object import GameObject
from interface import HealthBar
from idrawable import IDrawable


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

    def move(self, vector: Vector2):
        self.position += vector

    def get_position(self):
        return self.position

    def spawn_entities(self) -> [Entity]:
        entities = []
        stats = [0, 0, 0, 0, 0]
        for id in self.entities:
            entity = game_logic.get_entity(id)
            weapons = game_logic.get_weapons()
            entity.set_weapon(weapons[random.randint(0, len(weapons) - 1)])
            entity.stats.lvl = random.randint(0, 10)
            entity.stats.max_exp = entity.stats.exp * (entity.stats.lvl + 1)
            for i in range(entity.stats.lvl):
                stats[random.randint(0, len(stats) - 1)] += 1
            entity.stats.strength += stats[0]
            entity.stats.dexterity += stats[1]
            entity.stats.vitality += stats[2]
            entity.stats.endurance += stats[3]
            entity.stats.intellect += stats[4]
            entity.update_stats()
            entity.refresh()
            hp_bar = HealthBar(entity)
            game_cycle.game_data.game_interface.add_element(hp_bar)
            game_cycle.game_data.game_interface.add_element(entity.inventory)
            entities.append(entity)
        return entities

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass
