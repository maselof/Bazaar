import pygame.mixer

from hero import *
from chest import Chest
from trader import Trader


class Interface(IDrawable):
    elements: [IDrawable]

    def __init__(self):
        self.elements = []

    def add_element(self, element: IDrawable):
        self.elements.append(element)
        self.elements.sort(key=lambda el: el.priority)

    def update(self):
        for el in self.elements:
            el.update()
            if isinstance(el, HealthBar) and el.entity.is_dead:
                self.elements.remove(el)

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
        go, distance = game_cycle.game_data.game_map.get_nearest_object(self.hero)
        if not go or distance > self.hero.interact_radius:
            self.show = False
            return
        self.show = True
        if isinstance(go, Item):
            self.message = 'Take (E)'
        elif isinstance(go, Chest):
            self.message = 'Loot (E)'
        elif isinstance(go, Trader):
            self.message = 'Trade (E)'
        else:
            self.show = False

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


class MessageLog(IDrawable):
    message_queue: [[str, int]]
    symbol_height: int
    duration: int

    def __init__(self):
        self.message_queue = []
        self.symbol_height = game_logic.get_text_size('A', game_logic.ml_text_size).y
        self.duration = game_logic.ml_duration
        self.priority = game_logic.message_log_priority

    def add_message(self, message: str):
        self.message_queue.append([message, 0])

    def update(self):
        for m in self.message_queue:
            m[1] += 1
            if m[1] >= self.duration:
                self.message_queue.remove(m)

    def draw(self, screen: pygame.Surface):
        counter = 0
        count = len(self.message_queue)
        for m in self.message_queue:
            pos = Vector2(game_logic.ml_left_offset, game_logic.g_screen_center.y - (count - counter) * self.symbol_height)
            game_logic.print_text(screen, m[0], pos.x, pos.y, game_logic.ml_text_color, font_size=game_logic.ml_text_size)
            counter += 1


class HealthBar(IDrawable):
    __frame: ImageWrapper
    __band: ImageWrapper
    __offset: int
    __initial_band_size: int
    entity: Entity

    def __init__(self,
                 entity: Entity):
        self.entity = entity
        self.__offset = 20
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

        percent = max(self.entity.stats.hp / self.entity.stats.max_hp, 0)
        self.__band.set_size(pygame.Vector2(self.__initial_band_size * percent, self.__band.get_size().y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.__frame.image, self.__frame.rect)
        screen.blit(self.__band.image, self.__band.rect)
        lvl_text = f'LVL {self.entity.stats.lvl}'
        lvl_text_size = game_logic.get_text_size(lvl_text, game_logic.hb_lvl_text_size)
        lvl_text_pos = Vector2(self.__frame.get_position().x + (self.__frame.get_size().x - lvl_text_size.x) // 2, self.__frame.get_position().y - 20)
        game_logic.print_text(screen, lvl_text, lvl_text_pos.x, lvl_text_pos.y, game_logic.hb_text_color, font_size=game_logic.hb_lvl_text_size)


class SkillsPanel(IDrawable):
    hero: Hero
    show: bool
    old_attributes: {}
    new_attributes: {}
    stats: {}
    symbol_height: int
    size: Vector2

    current_attribute: int
    left_arrow: ImageWrapper
    right_arrow: ImageWrapper
    arrow_size: int

    def __init__(self, hero: Hero):
        self.hero = hero
        self.show = False
        self.priority = game_logic.skills_panel_priority
        self.symbol_height = game_logic.get_text_size('A', game_logic.sp_text_size).y
        self.open()
        self.close()
        self.size = Vector2(game_logic.sp_width, 2 * (game_logic.sp_layers_offset) + 3 * game_logic.sp_border_size +
                            self.symbol_height * (len(self.new_attributes) + len(self.stats)))
        self.current_attribute = 1
        self.left_arrow = ImageWrapper('res/images/interface/hero_stats/arrow_left.png')
        self.right_arrow = ImageWrapper('res/images/interface/hero_stats/arrow_right.png')
        self.arrow_size = self.left_arrow.image.get_size()[0]
        self.attributes_names = ['Skill points', 'Vitality', 'Endurance', 'Intellect', 'Strength', 'Dexterity']


    def get_stats_from_attributes(self):
        new_stats = Stats()
        new_stats.vitality = self.new_attributes.get('Vitality')
        new_stats.endurance = self.new_attributes.get('Endurance')
        new_stats.intellect = self.new_attributes.get('Intellect')
        new_stats.strength = self.new_attributes.get('Strength')
        new_stats.dexterity = self.new_attributes.get('Dexterity')
        new_stats.skill_points = self.new_attributes.get('Skill points')
        return new_stats

    def update_stats(self):
        stats = self.get_stats_from_attributes()
        h_s = self.hero.get_updated_stats(stats)
        self.stats = {'HP': f'{h_s.hp}/{h_s.max_hp}', 'SP': f'{h_s.stamina}/{h_s.max_stamina}', 'MP': f'{h_s.mana}/{h_s.max_mana}',
                      'Damage': str(h_s.damage), 'Attack Speed': str(h_s.attack_speed), 'DPS': str(h_s.dps), 'Speed': str(h_s.movement_speed)}

    def open(self):
        h_s = self.hero.stats
        self.old_attributes = {'Skill points': h_s.skill_points, 'Vitality': h_s.vitality, 'Endurance': h_s.endurance,
                               'Intellect': h_s.intellect, 'Strength': h_s.strength, 'Dexterity': h_s.dexterity}
        self.new_attributes = {'Skill points': h_s.skill_points, 'Vitality': h_s.vitality, 'Endurance': h_s.endurance,
                               'Intellect': h_s.intellect, 'Strength': h_s.strength, 'Dexterity': h_s.dexterity}
        self.update_stats()
        self.show = True

    def close(self):
        self.show = False

    def can_increase(self) -> bool:
        return self.new_attributes.get(self.attributes_names[0]) > 0

    def increase(self):
        if self.can_increase():
            self.new_attributes[self.attributes_names[self.current_attribute]] += 1
            self.new_attributes[self.attributes_names[0]] -= 1
            self.update_stats()

    def can_decrease(self) -> bool:
        name = self.attributes_names[self.current_attribute]
        return self.old_attributes[name] < self.new_attributes[name]

    def decrease(self):
        name = self.attributes_names[self.current_attribute]
        if self.can_decrease():
            self.new_attributes[name] -= 1
            self.new_attributes[self.attributes_names[0]] += 1
            self.update_stats()

    def save(self):
        a_s = self.get_stats_from_attributes()
        u_s = self.hero.get_updated_stats(a_s)
        h_s = self.hero.stats
        u_s.hp = h_s.hp
        u_s.stamina = h_s.stamina
        u_s.mana = h_s.mana
        u_s.exp = h_s.exp
        u_s.max_exp = h_s.max_exp
        u_s.lvl = h_s.lvl
        self.hero.stats = u_s
        self.hero.update_stats()
        self.close()

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        if not self.show:
            return

        first_layer_pos = game_logic.g_screen_center - self.size // 2
        pygame.draw.rect(screen, game_logic.sp_first_layer_color, Rect(first_layer_pos.x, first_layer_pos.y,
                                                                       self.size.x, self.size.y))

        border_size = self.size - Vector2(2, 2) * game_logic.sp_layers_offset
        border_pos = first_layer_pos + Vector2(1, 1) * game_logic.sp_layers_offset
        pygame.draw.rect(screen, game_logic.sp_border_color, Rect(border_pos.x, border_pos.y,
                                                                        border_size.x, border_size.y))

        second_layer_size = Vector2(border_size.x - 2 * game_logic.sp_border_size, len(self.new_attributes) * self.symbol_height)
        second_layer_pos = border_pos + Vector2(1, 1) * game_logic.sp_border_size
        pygame.draw.rect(screen, game_logic.sp_second_layer_color, Rect(second_layer_pos.x, second_layer_pos.y,
                                                                        second_layer_size.x, second_layer_size.y))

        i = 0
        name_pos = second_layer_pos + Vector2(game_logic.sp_text_offset, 0)
        for name, value in self.new_attributes.items():
            game_logic.print_text(screen, name, name_pos.x, name_pos.y, game_logic.sp_text_color, font_size=game_logic.sp_text_size)
            value_text = str(value)
            value_text_size = game_logic.get_text_size(value_text, game_logic.sp_text_size)
            value_text_pos = Vector2(second_layer_pos.x + second_layer_size.x - value_text_size.x - game_logic.sp_text_offset - self.arrow_size, name_pos.y)
            game_logic.print_text(screen, value_text, value_text_pos.x, value_text_pos.y, game_logic.sp_text_color, font_size=game_logic.sp_text_size)
            name_pos.y += self.symbol_height

            if i == self.current_attribute:
                if self.can_decrease():
                    self.left_arrow.set_position(value_text_pos - Vector2(self.arrow_size + game_logic.sp_arrow_offset.x, -1 * game_logic.sp_arrow_offset.y))
                    self.left_arrow.draw(screen)
                if self.can_increase():
                    self.right_arrow.set_position(value_text_pos + Vector2(value_text_size.x, 0) + game_logic.sp_arrow_offset)
                    self.right_arrow.draw(screen)
            i += 1

        second_layer_pos.y += second_layer_size.y + game_logic.sp_border_size
        second_layer_size = Vector2(border_size.x - 2 * game_logic.sp_border_size, len(self.stats) * self.symbol_height)
        pygame.draw.rect(screen, game_logic.sp_second_layer_color, Rect(second_layer_pos.x, second_layer_pos.y,
                                                                        second_layer_size.x, second_layer_size.y))

        name_pos = second_layer_pos + Vector2(game_logic.sp_text_offset, 0)
        for name, value in self.stats.items():
            game_logic.print_text(screen, name, name_pos.x, name_pos.y, game_logic.sp_text_color, font_size=game_logic.sp_text_size)
            value_text_size = game_logic.get_text_size(value, game_logic.sp_text_size)
            value_text_pos = Vector2(second_layer_pos.x + second_layer_size.x - value_text_size.x - game_logic.sp_text_offset, name_pos.y)
            game_logic.print_text(screen, value, value_text_pos.x, value_text_pos.y, game_logic.sp_text_color, font_size=game_logic.sp_text_size)
            name_pos.y += self.symbol_height


class HeroBars(IDrawable):
    hero: Hero

    def __init__(self,
                 hero: Hero):
        self.hero = hero
        self.priority = game_logic.hero_bars_priority

    def update(self):
        pass

    def draw_bar(self, screen: pygame.Surface, max: int, current: int, pos: Vector2, color):
        pygame.draw.rect(screen, game_logic.hb_frame_color, Rect(pos.x, pos.y, game_logic.hb_bar_size.x, game_logic.hb_bar_size.y))
        bar_size = Vector2(int(game_logic.hb_bar_size.x * current / max), game_logic.hb_bar_size.y)
        pygame.draw.rect(screen, color, Rect(pos.x, pos.y, bar_size.x, bar_size.y))

        text_pos = pos + Vector2(game_logic.hb_bar_size.x, 0)
        text = f'{current}/{max}'
        game_logic.print_text(screen, text, text_pos.x, text_pos.y, game_logic.hb_text_color, font_size=game_logic.hb_text_size)

    def draw(self, screen: pygame.Surface):
        bar_pos = Vector2(game_logic.g_screen_width - game_logic.hb_right_offset - game_logic.hb_bar_size.x,
                          game_logic.g_screen_height - game_logic.hb_bottom_offset - game_logic.hb_bar_size.y)
        self.draw_bar(screen, self.hero.stats.max_mana, self.hero.stats.mana, bar_pos, game_logic.hb_mana_color)

        exp_bar_pos = Vector2(game_logic.hb_right_offset, bar_pos.y)
        self.draw_bar(screen, self.hero.stats.max_exp, self.hero.stats.exp, exp_bar_pos, game_logic.hb_exp_bar_color)
        lvl_text = f'LVL {self.hero.stats.lvl}'
        lvl_height = game_logic.get_text_size(lvl_text, game_logic.hb_exp_text_size).y
        lvl_pos = exp_bar_pos - Vector2(0, lvl_height)
        game_logic.print_text(screen, lvl_text, lvl_pos.x, lvl_pos.y, game_logic.hb_text_color, font_size=game_logic.hb_exp_text_size)

        bar_pos.y -= game_logic.hb_bar_size.y + game_logic.hb_bars_offset
        self.draw_bar(screen, self.hero.stats.max_stamina, self.hero.stats.stamina, bar_pos, game_logic.hb_stamina_color)
        bar_pos.y -= game_logic.hb_bar_size.y + game_logic.hb_bars_offset
        self.draw_bar(screen, self.hero.stats.max_hp, self.hero.stats.hp, bar_pos, game_logic.hb_health_color)


class Button:

    size: Vector2
    position: Vector2
    text: str
    text_size: int

    def __init__(self, text: str, text_size: int, action):
        self.position = Vector2(0, 0)
        self.text = text
        self.text_size = text_size
        self.action = action
        self.size = game_logic.get_text_size(text, text_size)

    def draw(self, screen: pygame.Surface, is_active: bool):
        color = game_logic.menu_active_button_color if is_active else game_logic.menu_inactive_button_color
        game_logic.print_text(screen, self.text, self.position.x, self.position.y, color, font_size=self.text_size)


class Menu:
    buttons: [Button]
    current_button: int
    size: Vector2
    position: Vector2
    show: bool

    def __init__(self):
        buttons = [Button('New Game', game_logic.menu_buttons_text_size, self.hide),
                   Button('Load Game', game_logic.menu_buttons_text_size, self.load),
                   Button('Quit Game', game_logic.menu_buttons_text_size, pygame.quit)]
        self.show = True
        self.buttons = buttons
        self.current_button = 0
        c_b = len(self.buttons)
        b_h = self.buttons[0].size.y
        b_o = b_h + game_logic.menu_buttons_offset
        self.size = Vector2(game_logic.menu_width, c_b * b_o + game_logic.menu_buttons_offset + 2 * game_logic.menu_layers_offset)
        self.position = game_logic.g_screen_center - self.size // 2

        self.sl_size = self.size - Vector2(2, 2) * game_logic.menu_layers_offset
        self.sl_pos = self.position + Vector2(1, 1) * game_logic.menu_layers_offset

        for i in range(c_b):
            self.buttons[i].position = self.sl_pos + Vector2((self.sl_size.x - self.buttons[i].size.x) // 2,
                                                             game_logic.menu_buttons_offset + i * b_o)

    def do_action(self):
        self.buttons[self.current_button].action()

    def hide(self):
        self.show = False
        game_cycle.game_data.hero.change_context(Context.GAME)

    def load(self):
        game_cycle.load('quicksave')
        game_cycle.game_data.hero.change_context(Context.GAME)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, game_logic.menu_first_layer_color, Rect(self.position.x, self.position.y,
                                                                         self.size.x, self.size.y))

        pygame.draw.rect(screen, game_logic.menu_second_layer_color, Rect(self.sl_pos.x, self.sl_pos.y,
                                                                          self.sl_size.x, self.sl_size.y))

        for i in range(len(self.buttons)):
            self.buttons[i].draw(screen, i == self.current_button)
