import game_cycle
import game_logic
import interface
from idrawable import *
from image_wrapper import ImageWrapper
from pygame import Vector2
from game_object import GameObject
from entity import Entity
import random


def to_frame_coordinates(point: Vector2) -> Vector2:
    return Vector2(point.x // game_logic.map_frame_size.x, point.y // game_logic.map_frame_size.y)


def to_normal_coordinates(point: Vector2) -> Vector2:
    return Vector2(point.x * game_logic.map_frame_size.x, point.y * game_logic.map_frame_size.y)


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

    def __init__(self):
        game_logic.init_locations()

        self.all_frames = [MapFrame('res/images/map/backgrounds/grass.png', Vector2(0, 0))]
        self.central_frame = self.get_frame_by_pos(Vector2(0, 0))
        self.visible_frames = []
        self.all_game_objects = []
        self.visible_game_objects = []

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
            pos = start_frame.get_normal_position() + Vector2(position.x * game_logic.map_frame_size.x,
                                                              position.y * game_logic.map_frame_size.y)
        frame.set_normal_position(pos)
        self.all_frames.append(frame)

        location = game_logic.get_random_location()
        location.set_position(pos + Vector2(200, 200))
        for go in location.objects:
            self.add_game_object(go)
        entities = location.spawn_entities()
        for entity in entities:
            while True:
                pos = Vector2(random.randint(0, location.size.x) + location.position.x,
                              random.randint(0, location.size.y) + location.position.y)
                entity.set_position(pos)
                if not self.get_collided_all_objects(entity, [entity.collision_rect]):
                    break
            self.add_game_object(entity)

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

        if central_frame_position.x >= game_logic.g_screen_center.x:
            new_frame_offset.x = -1
        elif central_frame_position.x + game_logic.map_frame_size.x < game_logic.g_screen_center.x:
            new_frame_offset.x = 1

        if central_frame_position.y >= game_logic.g_screen_center.y:
            new_frame_offset.y = -1
        elif central_frame_position.y + game_logic.map_frame_size.y < game_logic.g_screen_center.y:
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
                if go.get_center().x >= frame.get_normal_position().x + game_logic.map_frame_size.x:
                    offset.x = 1
                elif go.get_center().x < frame.get_normal_position().x:
                    offset.x = -1

                if go.get_center().y >= frame.get_normal_position().y + game_logic.map_frame_size.y:
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
        frame_pos = to_frame_coordinates(game_object.get_position()- self.get_frame_by_pos(Vector2(0, 0)).get_normal_position())
        if not self.get_frame_by_pos(frame_pos):
            self.generate_frame(frame_pos)

        self.get_frame_by_pos(frame_pos).game_objects.append(game_object)
        self.all_game_objects.append(game_object)
        self.update_visible_objects()

    def remove_game_object(self, game_object: GameObject):
        frame_pos = to_frame_coordinates(game_object.get_position() - self.get_frame_by_pos(Vector2(0, 0)).get_normal_position())
        self.get_frame_by_pos(frame_pos).game_objects.remove(game_object)
        self.all_game_objects.remove(game_object)
        self.update_visible_objects()

    def check_dead(self):
        for go in self.visible_game_objects:
            if isinstance(go, Entity) and go.is_dead:
                self.remove_game_object(go)

    def move(self, vector: pygame.Vector2):
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

    def update(self):
        self.check_dead()
        f2 = self.check_objects_transitions()
        f1 = self.check_change_frame()
        if f1 | f2:
            self.update_visible_objects()

        self.visible_game_objects.sort(key=lambda go: go.collision_rect.bottom)

        for map_frame in self.visible_frames:
            map_frame.update()

    def draw(self, screen: pygame.Surface):
        for map_frame in self.visible_frames:
            map_frame.draw(screen)
        for go in self.visible_game_objects:
            go.draw(screen)
