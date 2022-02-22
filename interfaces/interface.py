import pygame
import game_cycle


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


def show_menu():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Игра")
    screen = pygame.display.set_mode((1680, 1050))
    menu_bg = pygame.image.load("res/images/bg.png")
    show = True
    start_button = Button(540, 100, screen)
    quit_button = Button(540, 100, screen)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bg, (0, 0))
        start_button.draw(300, 200, "Start Game", game_cycle.run, 70)
        quit_button.draw(300, 400, "Quit", pygame.quit, 70)
        pygame.display.update()





