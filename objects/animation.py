import pygame
import os


class Animation:
    path: str
    images: [pygame.Surface]
    speed: float
    frame: float
    frames_count: int
    finished: bool

    def __init__(self,
                 path: str,
                 speed: float = 1):
        self.path = path
        self.speed = speed
        self.frame = 0
        self.finished = True

        self.__load_images()
        self.frames_count = len(self.images)

    def __load_images(self):
        images = []
        for _, __, img_files in os.walk(self.path):
            for img in img_files:
                full_path = self.path + '/' + img
                images.append(pygame.image.load(full_path))
        self.images = images

    def start(self):
        self.frame = 0
        self.finished = False

    def get_current_frame(self):
        return self.images[int(self.frame)]

    def update(self):
        self.frame += self.speed
        if self.frame >= self.frames_count:
            self.frame = 0
            self.finished = True