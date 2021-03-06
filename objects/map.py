import random

import pygame
from pygame import Vector2

import game_cycle
import game_logic
from idrawable import IDrawable
from image_wrapper import ImageWrapper
from game_object import GameObject
from entity import Entity
from location import Location
from chest import Chest
from context import Context


def to_frame_coordinates(point: Vector2) -> Vector2:
    return Vector2(point.x // game_logic.MAP_FRAME_SIZE.x, point.y // game_logic.MAP_FRAME_SIZE.y)


def to_normal_coordinates(point: Vector2) -> Vector2:
    return Vector2(point.x * game_logic.MAP_FRAME_SIZE.x, point.y * game_logic.MAP_FRAME_SIZE.y)


class MapFrame(IDrawable):
    image: ImageWrapper
    game_objects: [GameObject]
    frame_position: Vector2

    def __init__(self,
                 bg_path: str,
                 position: Vector2):
        self.image = ImageWrapper(bg_path)
        self.game_objects = []
        self.frame_position = position
        self.image.set_position(to_normal_coordinates(position))

    def set_normal_position(self, position: Vector2):
        self.image.set_position(position)

    def get_normal_position(self) -> Vector2:
        return self.image.get_position()

    def move(self, vector: pygame.Vector2):
        self.image.move(vector)

    def update(self):
        for go in self.game_objects:
            go.update()

    def draw(self, screen: pygame.Surface):
        self.image.draw(screen)


class Map(IDrawable):
    all_frames: [MapFrame]
    visible_frames: [MapFrame]
    central_frame: MapFrame

    all_game_objects: [GameObject]
    visible_game_objects: [GameObject]
    hero: GameObject

    locations: [Location]

    def __init__(self, hero):
        self.locations = []
        self.all_frames = [MapFrame('res/images/map/backgrounds/grass.png', Vector2(0, 0))]
        self.central_frame = self.get_frame_by_pos(Vector2(0, 0))
        self.visible_frames = []
        self.all_game_objects = []
        self.visible_game_objects = []
        self.hero = hero
        self.change_central_frame(self.central_frame)

    def get_frame_by_pos(self, position: Vector2):
        for frame in self.all_frames:
            if frame.frame_position == position:
                return frame
        return None

    def generate_frame(self, position: Vector2) -> MapFrame:
        frame = MapFrame('res/images/map/backgrounds/grass.png', position)
        pos = Vector2(0, 0)
        start_frame = self.get_frame_by_pos(Vector2(0, 0))
        if start_frame:
            pos = start_frame.get_normal_position() + Vector2(position.x * game_logic.MAP_FRAME_SIZE.x,
                                                              position.y * game_logic.MAP_FRAME_SIZE.y)
        frame.set_normal_position(pos)
        self.all_frames.append(frame)

        location = game_logic.get_random_location()
        while True:
            location_pos = pos + Vector2(random.randint(0, game_logic.MAP_FRAME_SIZE.x),
                                         random.randint(0, game_logic.MAP_FRAME_SIZE.y))
            location.set_position(location_pos)
            for go in location.objects:
                if self.get_collided_all_objects(go, [go.collision_rect]):
                    continue
            break
        for go in location.objects:
            self.add_game_object(go)

        entities = location.spawn_entities()
        for entity in entities:
            while True:
                pos = Vector2(random.randint(0, int(location.size.x)) + location.position.x,
                              random.randint(0, int(location.size.y)) + location.position.y)
                entity.set_position(pos)
                if not self.get_collided_all_objects(entity, [entity.collision_rect]):
                    break
            entity.ai.movement_area = [Vector2(location.position), Vector2(location.position + location.size)]
            self.add_game_object(entity)

        self.locations.append(location)

        return frame

    def change_central_frame(self, frame: MapFrame):
        self.visible_frames.clear()
        self.central_frame = frame
        for x in range(-1, 2):
            for y in range(-1, 2):
                pos = frame.frame_position + Vector2(x, y)
                if not self.get_frame_by_pos(pos):
                    self.generate_frame(pos)
                self.visible_frames.append(self.get_frame_by_pos(pos))

    def check_change_frame(self) -> bool:
        new_frame_offset = Vector2(0, 0)
        central_frame_position = self.central_frame.image.get_position()

        if central_frame_position.x >= game_logic.SCREEN_CENTER.x:
            new_frame_offset.x = -1
        elif central_frame_position.x + game_logic.MAP_FRAME_SIZE.x < game_logic.SCREEN_CENTER.x:
            new_frame_offset.x = 1

        if central_frame_position.y >= game_logic.SCREEN_CENTER.y:
            new_frame_offset.y = -1
        elif central_frame_position.y + game_logic.MAP_FRAME_SIZE.y < game_logic.SCREEN_CENTER.y:
            new_frame_offset.y = 1

        if new_frame_offset != Vector2(0, 0):
            new_frame_pos = self.central_frame.frame_position + new_frame_offset
            frame = self.get_frame_by_pos(new_frame_pos)
            if not frame:
                frame = self.generate_frame(new_frame_pos)

            self.change_central_frame(frame)
            return True
        return False

    def check_objects_transitions(self) -> bool:
        flag = False
        for frame in self.visible_frames:
            for go in frame.game_objects:
                offset = Vector2(0, 0)
                if go.get_center().x >= frame.get_normal_position().x + game_logic.MAP_FRAME_SIZE.x:
                    offset.x = 1
                elif go.get_center().x < frame.get_normal_position().x:
                    offset.x = -1

                if go.get_center().y >= frame.get_normal_position().y + game_logic.MAP_FRAME_SIZE.y:
                    offset.y = 1
                elif go.get_center().y < frame.get_normal_position().y:
                    offset.y = -1

                if offset != Vector2(0, 0):
                    flag = True
                    new_pos = frame.frame_position + offset
                    new_frame = self.get_frame_by_pos(new_pos)
                    if not new_frame:
                        new_frame = self.generate_frame(new_pos)
                    frame.game_objects.remove(go)
                    new_frame.game_objects.append(go)
        return flag

    def update_visible_objects(self):
        self.visible_game_objects.clear()
        for frame in self.visible_frames:
            self.visible_game_objects.extend(frame.game_objects)

    def add_game_object(self, game_object: GameObject):
        frame_pos = to_frame_coordinates((game_object.get_center() -
                                          self.get_frame_by_pos(Vector2(0, 0)).get_normal_position()))
        if not self.get_frame_by_pos(frame_pos):
            self.generate_frame(frame_pos)

        self.get_frame_by_pos(frame_pos).game_objects.append(game_object)
        self.all_game_objects.append(game_object)
        self.update_visible_objects()

    def remove_game_object(self, game_object: GameObject):
        frame_pos = to_frame_coordinates((game_object.get_center() -
                                          self.get_frame_by_pos(Vector2(0, 0)).get_normal_position()))
        self.get_frame_by_pos(frame_pos).game_objects.remove(game_object)
        self.all_game_objects.remove(game_object)
        self.update_visible_objects()

    def check_to_remove(self):
        for go in self.visible_game_objects:
            if isinstance(go, Entity) and go.is_dead:
                bag = game_logic.get_game_object('bag')
                game_logic.fill_chest(bag, go.stats.lvl)
                if go.weapon.name != 'fists':
                    bag.inventory.add_item(go.weapon)

                bag.set_position(go.get_center())
                game_cycle.game_data.game_interface.add_element(bag.inventory)
                self.add_game_object(bag)
                go.stop_sounds()
                self.remove_game_object(go)
                self.hero.gain_exp(go.stats.max_exp)
                game_cycle.game_data.message_log.add_message(f'Gain {go.stats.max_exp} xp')
            if isinstance(go, Chest):
                if go.name == 'bag' and len(go.inventory.container) == 0:
                    if self.hero.inventory.is_open:
                        self.hero.change_context(Context.INVENTORY)
                    else:
                        self.hero.change_context(Context.GAME)
                    go.inventory.close()
                    self.remove_game_object(go)

    def move(self, vector: pygame.Vector2):
        for location in self.locations:
            location.move(vector)
        for map_frame in self.all_frames:
            map_frame.move(vector)

    def get_collided_all_objects(self, game_object: GameObject, area: [pygame.Rect]) -> [GameObject]:
        collided = []
        for go in self.all_game_objects:
            if go == game_object:
                continue

            for r in area:
                if go.collision_rect.colliderect(r):
                    collided.append(go)
                    break
        return collided

    def check_collisions(self, game_object: GameObject, vector: Vector2) -> Vector2:
        dir_vector = vector
        offset = Vector2(game_logic.COLLISION_OFFSET * (1 if dir_vector.x > 0 else -1 if dir_vector.x < 0 else 0),
                         game_logic.COLLISION_OFFSET * (1 if dir_vector.y > 0 else -1 if dir_vector.y < 0 else 0))
        collision_rect = game_object.collision_rect.copy()
        for go in self.visible_game_objects:
            if go == game_object:
                continue
            if dir_vector == Vector2(0, 0):
                return dir_vector
            if go.collision_rect.colliderect(collision_rect.move(vector.x + offset.x, 0)):
                dir_vector.x = 0
            if go.collision_rect.colliderect(collision_rect.move(0, vector.y + offset.y)):
                dir_vector.y = 0
            if dir_vector == Vector2(1, 1) and go.collision_rect.colliderect(
                    collision_rect.move(vector.x + offset.x, vector.y + offset.y)):
                dir_vector = Vector2(0, 0)
        return dir_vector

    def get_distance(self, object1: GameObject, object2: GameObject):
        return object1.get_center().distance_to(object2.get_center())

    def get_nearest_object(self, game_object: GameObject) -> [GameObject, float]:
        pos = game_object.get_center()

        min_distance = 1000000
        nearest_object = None
        if self.hero != game_object:
            min_distance = pos.distance_to(self.hero.get_center())
            nearest_object = self.hero

        for go in self.visible_game_objects:
            if go == game_object:
                continue

            go_pos = go.get_center()
            distance = go_pos.distance_to(pos)
            if distance < min_distance:
                min_distance = distance
                nearest_object = go
        return [nearest_object, min_distance]

    def get_collided_visible_objects(self, game_object: GameObject, area: [pygame.Rect]) -> [GameObject]:
        collided = []
        for go in self.visible_game_objects:
            if go == game_object:
                continue

            for r in area:
                if go.collision_rect.colliderect(r):
                    collided.append(go)
                    break
        return collided

    def update_sounds(self):
        for go in self.visible_game_objects:
            if go == self.hero:
                continue
            distance = game_cycle.game_data.game_map.get_distance(go, self.hero)
            if distance >= game_logic.HERO_SOUNDS_RANGE:
                continue
            k = 1 - distance / game_logic.HERO_SOUNDS_RANGE
            go.scale_sounds(k)

    def update(self):
        self.check_to_remove()
        f2 = self.check_objects_transitions()
        f1 = self.check_change_frame()
        if f1 | f2:
            self.update_visible_objects()

        self.visible_game_objects.sort(key=lambda go: go.collision_rect.bottom)

        for location in self.locations:
            location.update()

        for map_frame in self.visible_frames:
            map_frame.update()

        self.update_sounds()

    def draw(self, screen: pygame.Surface):
        for map_frame in self.visible_frames:
            map_frame.draw(screen)
        for location in self.locations:
            location.draw(screen)
        for go in self.visible_game_objects:
            go.draw(screen)
