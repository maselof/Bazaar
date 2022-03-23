from hero import *


class Camera:
    #map
    hero: Hero

    def __init__(self,
                 map,
                 hero: Hero):
        self.map = map
        self.hero = hero

    def update(self):
        back_vector = self.hero.direction_vector * -1 * self.hero.stats.movement_speed
        if back_vector == Vector2(0, 0):
            return
        self.map.move(back_vector)
        for go in self.map.all_game_objects:
            if go != self.hero:
                go.move(back_vector)

                if isinstance(go, Entity):
                    if go.ai.movement_area:

                        go.ai.movement_area[0] += back_vector
                        go.ai.movement_area[1] += back_vector
                    if go.ai.movement_point:
                        go.ai.movement_point.x += back_vector.x
                        go.ai.movement_point.y += back_vector.y

