import pygame.mixer
from pygame import Vector2
from pygame import Rect

import game_logic
import game_cycle
from hero import Hero
from chest import Chest
from trader import Trader
from idrawable import IDrawable
from item import Item
from image_wrapper import ImageWrapper
from entity import Entity
from entity import Stats
from context import Context


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
        self.priority = game_logic.DIALOG_WINDOW_PRIORITY

    def update(self):
        go, distance = game_cycle.game_data.game_map.get_nearest_object(self.hero)
        if not go or distance > self.hero.interact_radius:
            self.show = False
            return
        self.show = True
        if isinstance(go, Item):
            self.message = 'Take (E)'
        elif isinstance(go, Trader):
            self.message = 'Trade (E)'
        elif isinstance(go, Chest):
            self.message = 'Loot (E)'
        else:
            self.show = False

    def draw(self, screen: pygame.Surface):
        if not self.show:
            return

        text_size = game_logic.get_text_size(self.message, game_logic.DW_TEXT_SIZE)

        second_layer_size = text_size + game_logic.DW_TEXT_OFFSET * 2
        first_layer_size = second_layer_size + Vector2(2, 2) * game_logic.DW_LAYERS_OFFSET
        first_layer_pos = Vector2((game_logic.SCREEN_WIDTH - first_layer_size.x) // 2,
                                  game_logic.SCREEN_HEIGHT - game_logic.DW_BOTTOM_OFFSET)
        second_layer_pos = first_layer_pos + Vector2(1, 1) * game_logic.DW_LAYERS_OFFSET

        text_pos = second_layer_pos + (second_layer_size - text_size) // 2

        pygame.draw.rect(screen, game_logic.DW_FIRST_LAYER_COLOR, Rect(first_layer_pos.x, first_layer_pos.y,
                                                                       first_layer_size.x, first_layer_size.y))
        pygame.draw.rect(screen, game_logic.DW_SECOND_LAYER_COLOR, Rect(second_layer_pos.x, second_layer_pos.y,
                                                                        second_layer_size.x, second_layer_size.y))
        game_logic.print_text(screen, self.message, text_pos.x, text_pos.y,
                              game_logic.DW_TEXT_COLOR, font_size=game_logic.DW_TEXT_SIZE)


class MessageLog(IDrawable):
    message_queue: [[str, int]]
    symbol_height: int
    duration: int

    def __init__(self):
        self.message_queue = []
        self.symbol_height = game_logic.get_text_size('A', game_logic.ML_TEXT_SIZE).y
        self.duration = game_logic.ML_DURATION
        self.priority = game_logic.MESSAGE_LOG_PRIORITY

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
            pos = Vector2(game_logic.ML_LEFT_OFFSET,
                          game_logic.SCREEN_CENTER.y - (count - counter) * self.symbol_height)
            game_logic.print_text(screen, m[0], pos.x, pos.y,
                                  game_logic.ML_TEXT_COLOR, font_size=game_logic.ML_TEXT_SIZE)
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
        self.__initial_band_size = int(self.__band.get_size().x)
        self.priority = game_logic.HP_BAR_PRIORITY

    def center_x(self) -> int:
        bar_size = self.__frame.image.get_size()[0]
        entity_center = self.entity.get_position().x + self.entity.image.get_size()[0] // 2
        return int(entity_center - bar_size // 2)

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
        lvl_text_size = game_logic.get_text_size(lvl_text, game_logic.HB_LVL_TEXT_SIZE)
        lvl_text_pos = Vector2(self.__frame.get_position().x + (self.__frame.get_size().x - lvl_text_size.x) // 2,
                               self.__frame.get_position().y - 20)
        game_logic.print_text(screen, lvl_text, lvl_text_pos.x, lvl_text_pos.y,
                              game_logic.HB_TEXT_COLOR, font_size=game_logic.HB_LVL_TEXT_SIZE)


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
        self.priority = game_logic.SKILLS_PANEL_PRIORITY
        self.symbol_height = game_logic.get_text_size('A', game_logic.SP_TEXT_SIZE).y
        self.open()
        self.close()
        self.size = Vector2(game_logic.SP_WIDTH, 2 * game_logic.SP_LAYERS_OFFSET + 3 * game_logic.SP_BORDER_SIZE +
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
        self.stats = {'HP': f'{h_s.hp}/{h_s.max_hp}',
                      'SP': f'{h_s.stamina}/{h_s.max_stamina}', 'MP': f'{h_s.mana}/{h_s.max_mana}',
                      'Damage': str(h_s.damage), 'Attack Speed': str(h_s.attack_speed),
                      'DPS': str(h_s.dps), 'Speed': str(h_s.movement_speed)}

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

        first_layer_pos = game_logic.SCREEN_CENTER - self.size // 2
        pygame.draw.rect(screen, game_logic.SP_FIRST_LAYER_COLOR, Rect(first_layer_pos.x, first_layer_pos.y,
                                                                       self.size.x, self.size.y))

        border_size = self.size - Vector2(2, 2) * game_logic.SP_LAYERS_OFFSET
        border_pos = first_layer_pos + Vector2(1, 1) * game_logic.SP_LAYERS_OFFSET
        pygame.draw.rect(screen, game_logic.SP_BORDER_COLOR, Rect(border_pos.x, border_pos.y,
                                                                  border_size.x, border_size.y))

        second_layer_size = Vector2(border_size.x - 2 * game_logic.SP_BORDER_SIZE,
                                    len(self.new_attributes) * self.symbol_height)
        second_layer_pos = border_pos + Vector2(1, 1) * game_logic.SP_BORDER_SIZE
        pygame.draw.rect(screen, game_logic.SP_SECOND_LAYER_COLOR, Rect(second_layer_pos.x, second_layer_pos.y,
                                                                        second_layer_size.x, second_layer_size.y))

        i = 0
        name_pos = second_layer_pos + Vector2(game_logic.SP_TEXT_OFFSET, 0)
        for name, value in self.new_attributes.items():
            game_logic.print_text(screen, name, name_pos.x, name_pos.y,
                                  game_logic.SP_TEXT_COLOR, font_size=game_logic.SP_TEXT_SIZE)
            value_text = str(value)
            value_text_size = game_logic.get_text_size(value_text, game_logic.SP_TEXT_SIZE)
            value_text_pos = Vector2((second_layer_pos.x + second_layer_size.x - value_text_size.x
                                      - game_logic.SP_TEXT_OFFSET - self.arrow_size),
                                     name_pos.y)
            game_logic.print_text(screen, value_text, value_text_pos.x, value_text_pos.y,
                                  game_logic.SP_TEXT_COLOR, font_size=game_logic.SP_TEXT_SIZE)
            name_pos.y += self.symbol_height

            if i == self.current_attribute:
                if self.can_decrease():
                    self.left_arrow.set_position((value_text_pos -
                                                  Vector2(self.arrow_size + game_logic.SP_ARROW_OFFSET.x,
                                                          -1 * game_logic.SP_ARROW_OFFSET.y)))
                    self.left_arrow.draw(screen)
                if self.can_increase():
                    self.right_arrow.set_position((value_text_pos + Vector2(value_text_size.x, 0)
                                                   + game_logic.SP_ARROW_OFFSET))
                    self.right_arrow.draw(screen)
            i += 1

        second_layer_pos.y += second_layer_size.y + game_logic.SP_BORDER_SIZE
        second_layer_size = Vector2(border_size.x - 2 * game_logic.SP_BORDER_SIZE, len(self.stats) * self.symbol_height)
        pygame.draw.rect(screen, game_logic.SP_SECOND_LAYER_COLOR, Rect(second_layer_pos.x, second_layer_pos.y,
                                                                        second_layer_size.x, second_layer_size.y))

        name_pos = second_layer_pos + Vector2(game_logic.SP_TEXT_OFFSET, 0)
        for name, value in self.stats.items():
            game_logic.print_text(screen, name, name_pos.x, name_pos.y,
                                  game_logic.SP_TEXT_COLOR, font_size=game_logic.SP_TEXT_SIZE)
            value_text_size = game_logic.get_text_size(value, game_logic.SP_TEXT_SIZE)
            value_text_pos = Vector2((second_layer_pos.x + second_layer_size.x
                                      - value_text_size.x - game_logic.SP_TEXT_OFFSET),
                                     name_pos.y)
            game_logic.print_text(screen, value, value_text_pos.x, value_text_pos.y,
                                  game_logic.SP_TEXT_COLOR, font_size=game_logic.SP_TEXT_SIZE)
            name_pos.y += self.symbol_height


class HeroBars(IDrawable):
    hero: Hero

    def __init__(self,
                 hero: Hero):
        self.hero = hero
        self.priority = game_logic.HERO_BARS_PRIORITY

    def update(self):
        pass

    @staticmethod
    def draw_bar(screen: pygame.Surface, max_value: int, current_value: int, pos: Vector2, color):
        pygame.draw.rect(screen, game_logic.HB_FRAME_COLOR, Rect(pos.x, pos.y, game_logic.HB_BAR_SIZE.x,
                                                                 game_logic.HB_BAR_SIZE.y))
        bar_size = Vector2(int(game_logic.HB_BAR_SIZE.x * current_value / max_value), game_logic.HB_BAR_SIZE.y)
        pygame.draw.rect(screen, color, Rect(pos.x, pos.y, bar_size.x, bar_size.y))

        text_pos = pos + Vector2(game_logic.HB_BAR_SIZE.x, 0)
        text = f'{current_value}/{max_value}'
        game_logic.print_text(screen, text, text_pos.x, text_pos.y,
                              game_logic.HB_TEXT_COLOR, font_size=game_logic.HB_TEXT_SIZE)

    def draw(self, screen: pygame.Surface):
        bar_pos = Vector2(game_logic.SCREEN_WIDTH - game_logic.HB_RIGHT_OFFSET - game_logic.HB_BAR_SIZE.x,
                          game_logic.SCREEN_HEIGHT - game_logic.HB_BOTTOM_OFFSET - game_logic.HB_BAR_SIZE.y)
        self.draw_bar(screen, self.hero.stats.max_mana, self.hero.stats.mana, bar_pos, game_logic.HB_MANA_COLOR)

        exp_bar_pos = Vector2(game_logic.HB_RIGHT_OFFSET, bar_pos.y)
        self.draw_bar(screen, self.hero.stats.max_exp, self.hero.stats.exp, exp_bar_pos, game_logic.HB_EXP_BAR_COLOR)
        lvl_text = f'LVL {self.hero.stats.lvl}'
        lvl_height = game_logic.get_text_size(lvl_text, game_logic.HB_EXP_TEXT_SIZE).y
        lvl_pos = exp_bar_pos - Vector2(0, lvl_height)
        game_logic.print_text(screen, lvl_text, lvl_pos.x, lvl_pos.y,
                              game_logic.HB_TEXT_COLOR, font_size=game_logic.HB_EXP_TEXT_SIZE)

        bar_pos.y -= game_logic.HB_BAR_SIZE.y + game_logic.HB_BARS_OFFSET
        self.draw_bar(screen, self.hero.stats.max_stamina, self.hero.stats.stamina, bar_pos,
                      game_logic.HB_STAMINA_COLOR)
        bar_pos.y -= game_logic.HB_BAR_SIZE.y + game_logic.HB_BARS_OFFSET
        self.draw_bar(screen, self.hero.stats.max_hp, self.hero.stats.hp, bar_pos, game_logic.HB_HEALTH_COLOR)


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
        color = game_logic.MENU_ACTIVE_BUTTON_COLOR if is_active else game_logic.MENU_INACTIVE_BUTTON_COLOR
        game_logic.print_text(screen, self.text, self.position.x, self.position.y, color, font_size=self.text_size)


class DeathMessage:

    position: Vector2
    text: str
    text_pos: Vector2
    size: Vector2

    def __init__(self):
        self.text = 'You died! (Press ENTER)'
        self.size = game_logic.DM_SIZE
        self.position = game_logic.SCREEN_CENTER - self.size // 2
        self.text_pos = self.position + (self.size - Vector2(2, 2) * game_logic.MENU_LAYERS_OFFSET -
                                         game_logic.get_text_size(self.text, game_logic.MENU_BUTTONS_TEXT_SIZE)) // 2
        self.sl_pos = self.position + Vector2(1, 1) * game_logic.MENU_LAYERS_OFFSET
        self.sl_size = self.size - Vector2(2, 2) * game_logic.MENU_LAYERS_OFFSET

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, game_logic.MENU_FIRST_LAYER_COLOR, Rect(self.position.x, self.position.y,
                                                                         self.size.x, self.size.y))
        pygame.draw.rect(screen, game_logic.MENU_SECOND_LAYER_COLOR, Rect(self.sl_pos.x, self.sl_pos.y,
                                                                          self.sl_size.x, self.sl_size.y))
        game_logic.print_text(screen, self.text, self.text_pos.x, self.text_pos.y,
                              (255, 255, 255), font_size=game_logic.MENU_BUTTONS_TEXT_SIZE)


class Menu:
    buttons: [Button]
    current_button: int
    size: Vector2
    position: Vector2
    show: bool

    def __init__(self):
        buttons = [Button('New Game', game_logic.MENU_BUTTONS_TEXT_SIZE, self.hide),
                   Button('Load Game', game_logic.MENU_BUTTONS_TEXT_SIZE, self.load),
                   Button('Quit Game', game_logic.MENU_BUTTONS_TEXT_SIZE, pygame.quit)]
        self.show = True
        self.buttons = buttons
        self.current_button = 0
        c_b = len(self.buttons)
        b_h = self.buttons[0].size.y
        b_o = b_h + game_logic.MENU_BUTTONS_OFFSET
        self.size = Vector2(game_logic.MENU_WIDTH,
                            c_b * b_o + game_logic.MENU_BUTTONS_OFFSET + 2 * game_logic.MENU_LAYERS_OFFSET)
        self.position = game_logic.SCREEN_CENTER - self.size // 2

        self.sl_size = self.size - Vector2(2, 2) * game_logic.MENU_LAYERS_OFFSET
        self.sl_pos = self.position + Vector2(1, 1) * game_logic.MENU_LAYERS_OFFSET

        for i in range(c_b):
            self.buttons[i].position = self.sl_pos + Vector2((self.sl_size.x - self.buttons[i].size.x) // 2,
                                                             game_logic.MENU_BUTTONS_OFFSET + i * b_o)

    def do_action(self):
        self.buttons[self.current_button].action()

    def hide(self):
        game_cycle.game_data.init()
        self.show = False
        game_cycle.game_data.hero.change_context(Context.START)
        game_cycle.game_data.hero.change_context(Context.GAME)

    def load(self):
        game_cycle.load('quicksave')
        game_cycle.game_data.hero.change_context(Context.START)
        game_cycle.game_data.hero.change_context(Context.GAME)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, game_logic.MENU_FIRST_LAYER_COLOR, Rect(self.position.x, self.position.y,
                                                                         self.size.x, self.size.y))

        pygame.draw.rect(screen, game_logic.MENU_SECOND_LAYER_COLOR, Rect(self.sl_pos.x, self.sl_pos.y,
                                                                          self.sl_size.x, self.sl_size.y))

        for i in range(len(self.buttons)):
            self.buttons[i].draw(screen, i == self.current_button)
