import pygame
from entity import Entity
from image_wrapper import ImageWrapper
from idrawable import *


class Interface(IDrawable):
    elements: [IDrawable]

    def __init__(self):
        self.elements = []

    def update(self):
        for el in self.elements:
            el.update()

    def draw(self, screen: pygame.Surface):
        for el in self.elements:
            el.draw(screen)


class HealthBar(IDrawable):
    __frame: ImageWrapper
    __band: ImageWrapper
    __offset: int
    __initial_band_size: int
    entity: Entity

    def __init__(self,
                 entity: Entity):
        self.entity = entity
        self.__offset = -10
        self.__frame = ImageWrapper('res/images/interface/health_bar/frame.png')
        self.__band = ImageWrapper('res/images/interface/health_bar/band.png')
        self.__frame.scale(0.7, 0.5)
        self.__band.scale(0.7, 0.5)
        self.__initial_band_size = int(self.__band.get_size().x)

    def center_x(self) -> int:
        bar_size = self.__frame.image.get_size()[0]
        entity_center = self.entity.get_position().x + self.entity.image.get_size()[0] // 2
        return entity_center - bar_size // 2

    def update(self):
        pos = pygame.Vector2(self.center_x(), self.entity.get_position().y + self.__offset)
        self.__frame.set_position(pos)
        self.__band.set_position(pos)

        percent = max(self.entity.hp / self.entity.max_hp, 0)
        self.__band.set_size(pygame.Vector2(self.__initial_band_size * percent, self.__band.get_size().y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.__frame.image, self.__frame.rect)
        screen.blit(self.__band.image, self.__band.rect)


class Button:
    def __init__(self, w, h, screen):
        """инициализация кнопки"""
        self.w = w
        self.h = h
        self.inactive_color = (120, 120, 120)
        self.active_color = (60, 60, 60)
        self.screen = screen

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(self.screen, self.active_color, (x, y, self.w, self.h))
            if click[0]:
                action()
        else:
            pygame.draw.rect(self.screen, self.inactive_color, (x, y, self.w, self.h))
        print_text(self.screen, message=message, x=x + 10, y=y + 10, font_size=font_size)


def print_text(screen, message, x, y, font_color=(0, 0, 0), font_type="res/fonts/a_Alterna.ttf", font_size=30):

    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def pause(screen):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text(screen, "Press ENTER to continue", 160, 200)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()





