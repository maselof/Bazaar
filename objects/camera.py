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
        back_vector = self.hero.direction_vector * -1 * self.hero.speed
        self.map.move(back_vector)
        for go in self.map.game_objects:
            go.move(back_vector)
