import pygame
from game_object import *


class Item(GameObject):
    id: int

    def __init__(self, id: int):
        super().__init__()
        self.id = id
