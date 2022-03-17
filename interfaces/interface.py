from inventory import *
from hero import *


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


class DialogWindow(IDrawable):
    message: str
    show: bool
    priority: int
    hero: Hero

    def __init__(self,
                 hero: Hero):
        self.message = ''
        self.hero = hero
        self.show = False
        self.priority = game_logic.dialog_window_priority

    def update(self):
        go, distance = game_cycle.get_nearest_object(self.hero)
        if not go or distance > self.hero.interact_radius:
            self.show = False
            return
        self.show = True
        if isinstance(go, Item):
            self.message = 'Take (E)'
        elif isinstance(go, ILootable):
            self.message = 'Loot (E)'

    def draw(self, screen: pygame.Surface):
        if not self.show:
            return

        text_size = game_logic.get_text_size(self.message, game_logic.dw_text_size)

        second_layer_size = text_size + game_logic.dw_text_offset * 2
        first_layer_size = second_layer_size + Vector2(2, 2) * game_logic.dw_layers_offset
        first_layer_pos = Vector2((game_logic.g_screen_width - first_layer_size.x) // 2, game_logic.g_screen_height - game_logic.dw_bottom_offset)
        second_layer_pos = first_layer_pos + Vector2(1, 1) * game_logic.dw_layers_offset

        text_pos = second_layer_pos + (second_layer_size - text_size) // 2

        pygame.draw.rect(screen, game_logic.dw_first_layer_color, Rect(first_layer_pos.x, first_layer_pos.y,
                                                                       first_layer_size.x, first_layer_size.y))
        pygame.draw.rect(screen, game_logic.dw_second_layer_color, Rect(second_layer_pos.x, second_layer_pos.y,
                                                                        second_layer_size.x, second_layer_size.y))
        game_logic.print_text(screen, self.message, text_pos.x, text_pos.y,game_logic.dw_text_color, font_size=game_logic.dw_text_size)


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
        self.priority = game_logic.hp_bar_priority

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

        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(self.screen, self.active_color, (x, y, self.w, self.h))
            if click[0]:
                action()
        else:
            pygame.draw.rect(self.screen, self.inactive_color, (x, y, self.w, self.h))
        game_logic.print_text(self.screen, message=message, x=x + 10, y=y + 10, font_size=font_size)


def pause(screen):
    paused = True
    quit_button = Button(540, 100, screen)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_logic.print_text(screen, "Press ENTER to continue", screen.get_size()[0] // 2 - 150, screen.get_size()[1] // 2 - 100)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        quit_button.draw(screen.get_size()[0] // 2 - 250, screen.get_size()[1] // 2, "Quit", pygame.quit, 70)
        pygame.display.update()


pygame.init()






