import pygame


class Hero:

    def __init__(self, screen):
        """инициализация игрока"""

        self.screen = screen
        self.image = pygame.image.load("data/image/3.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.centerX = float(self.rect.centerx)
        self.rect.centery = self.screen_rect.centery
        self.centerY = float(self.rect.centery)
        self.mright = False
        self.mleft = False
        self.mup = False
        self.mdown = False
        self.i = 0

    def output(self):
        """вывод игрока на экран"""
        self.screen.blit(self.image, self.rect)
        # анимация игрока
        walk_right = [pygame.image.load("data/image/7.png"), pygame.image.load("data/image/8.png")]
        walk_left = [pygame.image.load("data/image/5.png"), pygame.image.load("data/image/6.png")]
        walk_up = [pygame.image.load("data/image/1.png"), pygame.image.load("data/image/2.png")]
        walk_down = [pygame.image.load("data/image/3.png"), pygame.image.load("data/image/4.png")]
        if self.mright:
            self.image = walk_right[self.i // 30]
            self.i += 1
            if self.i + 1 > 60:
                self.i = 0

        if self.mleft:
            self.image = walk_left[self.i // 30]
            self.i += 1
            if self.i + 1 > 60:
                self.i = 0

        if self.mup:
            self.image = walk_up[self.i // 30]
            self.i += 1
            if self.i + 1 > 60:
                self.i = 0

        if self.mdown:
            self.image = walk_down[self.i // 30]
            self.i += 1
            if self.i + 1 > 60:
                self.i = 0

    def update_hero(self, screen):
        """движение игрока"""
        if self.mright and self.rect.right < self.screen_rect.right:
            self.centerX += 3
        if self.mleft and self.rect.left > 0:
            self.centerX -= 3
        if self.mdown and self.rect.height < self.screen_rect.height:
            self.centerY += 3
        if self.mup and self.rect.height > 0:
            self.centerY -= 3

        self.rect.centerx = self.centerX
        self.rect.centery = self.centerY
