import pygame


class Animation:
    path: str
    images: [pygame.Surface]
    speed: float
    frame: float
    finished: bool
    frames_count: int

    def __init__(self,
                 path: str,
                 speed: float = 1):
        self.path = path
        self.speed = speed
        self.frame = 0
        self.finished = True
        self.frames_count = len(self.images)

    def __load_images(self):


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