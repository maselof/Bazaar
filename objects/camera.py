from hero import *


class Camera:
    #map
    hero: Hero

    def __init__(self,
                 map,
                 hero: Hero):
        self.map = map
        self.hero = hero

    def check_collisions(self, vector: Vector2) -> Vector2:
        dir_vector = vector
        for go in self.map.game_objects:
            if dir_vector == Vector2(0, 0):
                return dir_vector
            if self.hero.collision_rect.colliderect(go.collision_rect.move(vector.x, 0)):
                dir_vector.x = 0
            if self.hero.collision_rect.colliderect(go.collision_rect.move(0, vector.y)):
                dir_vector.y = 0
        return dir_vector

    def update(self):
        back_vector = self.hero.direction_vector * -1 * self.hero.speed
        back_vector = self.check_collisions(back_vector)
        if back_vector == Vector2(0, 0):
            return

        self.map.move(back_vector)
        for go in self.map.game_objects:
            go.move(back_vector)

