import pygame
import os
from direction import *


class Animation:
    path: str
    name: str
    images: []
    speed: float
    frame: float
    finished: bool
    interruptable: bool
    directional: bool

    def __init__(self,
                 path: str,
                 name: str,
                 directional: bool = True,
                 interruptible: bool = True,
                 speed: float = 1,
                 scale: float = 1):
        self.path = path + name
        self.name = name
        self.interruptable = interruptible
        self.directional = directional
        self.speed = speed
        self.scale = scale
        self.frame = 0
        self.finished = True

        self.__prepare_images()

    def __prepare_images(self):
        if self.directional:
            self.images = {Direction.LEFT: self.__load_images('left/'),
                           Direction.RIGHT: self.__load_images('right/'),
                           Direction.UP: self.__load_images('up/'),
                           Direction.DOWN: self.__load_images('down/')}
        else:
            self.images = {Direction.STAND: self.__load_images('')}

    def __load_images(self, dir: str):
        images = []
        dir_path = self.path + '/' + dir
        for _, __, img_files in os.walk(dir_path):
            for img in img_files:
                full_path = dir_path + img
                images.append(pygame.image.load(full_path).convert_alpha())
        return images

    def start(self):
        self.frame = 0
        self.finished = False

    def get_current_frame(self, direction: Direction):
        if int(self.frame) >= len(self.images.get(direction)):
            self.frame = 0
            self.finished = True
        return self.images.get(direction)[int(self.frame)]

    def update(self, direction: Direction):
        self.frame += self.speed

    def __getstate__(self):
        return self.path, self.name, self.speed, self.frame, self.finished, self.interruptable, self.directional

    def __setstate__(self, state):
        self.path, self.name, self.speed, self.frame, self.finished, self.interruptable, self.directional = state
        self.__prepare_images()
