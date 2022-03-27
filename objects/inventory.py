import pygame
from pygame import Vector2

import game_logic
from image_wrapper import ImageWrapper
from idrawable import IDrawable
from weapon import Weapon
from item import Item


class DescriptionWindow(IDrawable):
    bg_pos: Vector2
    size: Vector2
    item: Item
    icon_frame: ImageWrapper

    def __init__(self):
        self.size = game_logic.DSCW_SIZE
        self.bg_pos = Vector2((game_logic.SCREEN_WIDTH - self.size.x) // 2, game_logic.INVENTORY_TOP_OFFSET)
        self.icon_frame = ImageWrapper(path='res/images/interface/inventory/inv_cell.png')

    def update(self):
        pass

    def draw_description(self, screen: pygame.Surface, description: str, pos: Vector2, max_width: int, font_size: int):
        words = description.split()
        space_size = game_logic.get_text_size(' ', font_size)
        current_width = 0
        for word in words:
            word_size = game_logic.get_text_size(word, font_size)
            if current_width + word_size.x > max_width:
                current_width = 0
                pos.y += space_size.y
            game_logic.print_text(screen, word, pos.x + current_width, pos.y,
                                  game_logic.DW_TEXT_COLOR, font_size=font_size)
            current_width += word_size.x + space_size.x

    def draw_stat(self, screen: pygame.Surface, stat_name: str, stat_value: str, pos: Vector2, right_border: int):
        game_logic.print_text(screen, stat_name, pos.x, pos.y,
                              game_logic.DW_TEXT_COLOR, font_size=game_logic.DSCW_STATS_TEXT_SIZE)
        value = str(stat_value)
        value_pos = Vector2(right_border - game_logic.get_text_size(value, game_logic.DSCW_STATS_TEXT_SIZE).x, pos.y)
        game_logic.print_text(screen, value, value_pos.x, value_pos.y,
                              game_logic.DW_TEXT_COLOR, font_size=game_logic.DSCW_STATS_TEXT_SIZE)

    def draw(self, screen: pygame.Surface):
        if not self.item:
            return

        pygame.draw.rect(screen, game_logic.INVENTORY_BACKGROUND_COLOR, pygame.Rect(self.bg_pos.x, self.bg_pos.y,
                                                                                    self.size.x, self.size.y))

        text_name = self.item.name
        text_name_size = game_logic.get_text_size(text_name, game_logic.DW_TEXT_SIZE)
        text_name_pos = self.bg_pos + Vector2((self.size.x - text_name_size.x) // 2, 0)
        game_logic.print_text(screen, text_name, text_name_pos.x, text_name_pos.y,
                              game_logic.DW_TEXT_COLOR, font_size=game_logic.DW_TEXT_SIZE)

        second_layer_size = self.size - Vector2(2 * game_logic.DW_LAYERS_OFFSET,
                                                text_name_size.y + game_logic.DW_LAYERS_OFFSET)
        second_layer_pos = self.bg_pos + Vector2(game_logic.DW_LAYERS_OFFSET, text_name_size.y)
        pygame.draw.rect(screen, game_logic.DW_SECOND_LAYER_COLOR,
                         pygame.Rect(second_layer_pos.x, second_layer_pos.y,
                                     second_layer_size.x, second_layer_size.y))

        self.icon_frame.set_position(second_layer_pos)
        self.icon_frame.draw(screen)
        icon = ImageWrapper(self.item.icon.path, self.item.icon.size)
        icon.set_position(second_layer_pos + Vector2(1, 1) * game_logic.DSCW_FRAME_ICON_OFFSET)
        icon.draw(screen)

        description = self.item.description
        description_pos = (second_layer_pos +
                           Vector2(game_logic.DSCW_FRAME_ICON_OFFSET * 2 + game_logic.PANEL_ITEMS_SIZE, 0) +
                           Vector2(1, 1) * game_logic.DSCW_DESCRIPTION_OFFSET)
        max_width = int(second_layer_pos.x + second_layer_size.x - description_pos.x)
        self.draw_description(screen, description, description_pos, max_width, game_logic.DSCW_DESCRIPTION_TEXT_SIZE)

        stats_pos = (second_layer_pos +
                     Vector2(0, game_logic.DSCW_FRAME_ICON_OFFSET * 2 + game_logic.PANEL_ITEMS_SIZE) +
                     Vector2(1, 1) * game_logic.DSCW_DESCRIPTION_OFFSET)
        stats_right_border = second_layer_pos.x + second_layer_size.x - game_logic.DSCW_DESCRIPTION_OFFSET
        symbol_height = game_logic.get_text_size('A', game_logic.DSCW_STATS_TEXT_SIZE).y

        if isinstance(self.item, Weapon):
            self.draw_stat(screen, 'Damage', str(self.item.damage), stats_pos, stats_right_border)
            stats_pos.y += symbol_height
            self.draw_stat(screen, 'Attack Speed Modifier', str(self.item.attack_speed_modifier),
                           stats_pos, stats_right_border)
            stats_pos.y += symbol_height
            self.draw_stat(screen, 'Range', str(self.item.attack_range), stats_pos, stats_right_border)
            stats_pos.y += symbol_height

        for effect in self.item.effects:
            self.draw_stat(screen, effect.name, str(effect.value), stats_pos, stats_right_border)
            stats_pos.y += symbol_height

        cost_text_pos = (second_layer_pos +
                         Vector2(0, second_layer_size.y - symbol_height) +
                         Vector2(1, -1) * game_logic.DSCW_DESCRIPTION_OFFSET)
        game_logic.print_text(screen, 'Value', cost_text_pos.x, cost_text_pos.y,
                              game_logic.DSCW_COST_TEXT_COLOR, font_size=game_logic.DSCW_STATS_TEXT_SIZE)
        cost = str(self.item.cost)
        cost_pos = Vector2(stats_right_border - game_logic.get_text_size(cost, game_logic.DSCW_STATS_TEXT_SIZE).x,
                           cost_text_pos.y)
        game_logic.print_text(screen, cost, cost_pos.x, cost_pos.y,
                              game_logic.DSCW_COST_TEXT_COLOR, font_size=game_logic.DSCW_STATS_TEXT_SIZE)


class GameContainer(IDrawable):
    container: [Item]
    bg_pos: Vector2
    is_open: bool
    show_frame: bool
    focus_item_index: int
    description_window: DescriptionWindow

    def __init__(self):
        self.container = []
        self.inv_cell_img = ImageWrapper('res/images/interface/inventory/inv_cell.png')
        self.frame_img = ImageWrapper('res/images/interface/inventory/frame.png')
        self.is_open = False
        self.show_frame = False
        self.focus_item_index = 0
        width, height = self.inv_cell_img.get_size()
        self.inv_cell_rect = pygame.Rect(0, 0, width, height)
        self.bg_pos = (Vector2((game_logic.SCREEN_WIDTH -
                                self.inv_cell_rect.size[0] * game_logic.INVENTORY_COLUMNS_COUNT), 0) +
                       Vector2(-1, 1) * game_logic.INVENTORY_TOP_OFFSET)
        self.priority = game_logic.INVENTORY_PRIORITY
        self.description_window = DescriptionWindow()

    def close(self):
        self.is_open = False
        self.show_frame = False

    def open(self):
        self.is_open = True
        self.show_frame = True

    def change_focus_item(self, index: int):
        new_index = self.focus_item_index + index
        if (new_index < 0) | (new_index >= len(self.container)):
            return
        self.focus_item_index = new_index

    def get_item(self, index: int):
        if index < 0 or index >= len(self.container):
            return None
        return self.container[index]

    def get_focus_item(self):
        if self.focus_item_index >= len(self.container):
            return None
        return self.container[self.focus_item_index]

    def add_item(self, item: Item, count: int = 1):
        for i in self.container:
            if i.name == item.name:
                if isinstance(item, Weapon) and isinstance(i, Weapon) and item.is_equipped != i.is_equipped:
                    continue
                i.count += count
                if item.bottom_panel_index != 0:
                    i.bottom_panel_index = item.bottom_panel_index
                return
        new_item = game_logic.get_item(item.name)
        new_item.bottom_panel_index = item.bottom_panel_index
        if isinstance(new_item, Weapon):
            new_item.set_equipped(item.is_equipped)
        new_item.count = count
        self.container.append(new_item)

    def remove_item(self, item: Item, count: int = 1):
        for i in self.container:
            if i.name == item.name:
                if isinstance(item, Weapon) and isinstance(i, Weapon) and item.is_equipped != i.is_equipped:
                    continue
                i.count -= count

    def update(self):
        for item in self.container:
            if item.count <= 0:
                self.container.remove(item)
        self.description_window.update()

    def draw(self, screen: pygame.Surface):
        if not self.is_open:
            return

        raws_count = max(len(self.container) // game_logic.INVENTORY_COLUMNS_COUNT + 1,
                         game_logic.INVENTORY_MIN_RAWS_COUNT)
        cells_count = raws_count * game_logic.INVENTORY_COLUMNS_COUNT

        bg_size = (Vector2(self.inv_cell_rect.size[0] * game_logic.INVENTORY_COLUMNS_COUNT,
                           self.inv_cell_rect.size[1] * raws_count) +
                   2 * Vector2(game_logic.INVENTORY_LEFT_CELL_OFFSET, game_logic.INVENTORY_LEFT_CELL_OFFSET))

        pygame.draw.rect(screen, game_logic.INVENTORY_BACKGROUND_COLOR, pygame.Rect(self.bg_pos, bg_size))

        img_width, img_height = self.inv_cell_rect.size

        for i in range(cells_count):
            pos = self.bg_pos + Vector2((img_width * (i % game_logic.INVENTORY_COLUMNS_COUNT) +
                                         game_logic.INVENTORY_LEFT_CELL_OFFSET),
                                        (img_height * (i // game_logic.INVENTORY_COLUMNS_COUNT) +
                                         game_logic.INVENTORY_LEFT_CELL_OFFSET))
            self.inv_cell_rect.x, self.inv_cell_rect.y = pos.x, pos.y
            screen.blit(self.inv_cell_img.image, self.inv_cell_rect)
            if i < len(self.container):
                el_pos = pos + Vector2(1, 1) * game_logic.INVENTORY_LEFT_CELL_OFFSET
                self.container[i].icon.set_position(el_pos)
                self.container[i].icon.draw(screen)

                count = str(self.container[i].count)
                count_text_size = game_logic.get_text_size(count, game_logic.INVENTORY_TEXT_SIZE)
                item_icon_size = Vector2(1, 1) * game_logic.PANEL_ITEMS_SIZE
                count_text_pos = el_pos + item_icon_size - count_text_size
                game_logic.print_text(screen, count, count_text_pos.x, count_text_pos.y,
                                      game_logic.PANEL_COUNT_COLOR, font_size=game_logic.INVENTORY_TEXT_SIZE)

                bpi = self.container[i].bottom_panel_index
                if bpi > 0:
                    game_logic.print_text(screen, str(bpi), el_pos.x, el_pos.y,
                                          game_logic.PANEL_NUMBER_COLOR, font_size=game_logic.INVENTORY_TEXT_SIZE)

        if self.show_frame:
            cell_size = Vector2(self.inv_cell_rect.size[0])
            frame_pos = (self.bg_pos +
                         Vector2(1, 1) * game_logic.INVENTORY_LEFT_CELL_OFFSET +
                         Vector2((self.focus_item_index % 5) * cell_size.x,
                                 (self.focus_item_index // 5) * cell_size.y))
            self.frame_img.set_position(frame_pos)
            self.frame_img.draw(screen)

        if not self.show_frame:
            self.description_window.item = None
        else:
            self.description_window.item = self.get_focus_item()

        self.description_window.draw(screen)


class HeroInventory(GameContainer):
    inventory_panel = [Item]

    def __init__(self):
        super().__init__()
        self.inventory_panel = [None for i in range(game_logic.PANEL_ITEMS_COUNT)]
        self.ip_image = ImageWrapper('res/images/interface/inventory/items_panel.png')
        ip_w, ip_h = self.ip_image.get_size()
        self.ip_rect = pygame.Rect((game_logic.SCREEN_WIDTH - ip_w) // 2,
                                   game_logic.SCREEN_HEIGHT - ip_h - game_logic.PANEL_BOTTOM_OFFSET, 0, 0)
        self.bg_pos = Vector2(game_logic.INVENTORY_TOP_OFFSET, game_logic.INVENTORY_TOP_OFFSET)

    def update(self):
        super().update()
        for i in range(len(self.inventory_panel)):
            if self.inventory_panel[i] and self.inventory_panel[i].count == 0:
                self.inventory_panel[i] = None

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        self.draw_inventory_panel(screen)

    def update_panel(self):
        self.inventory_panel = [None for i in range(game_logic.PANEL_ITEMS_COUNT)]
        for i in self.container:
            if i.bottom_panel_index > 0 and i.count > 0:
                self.inventory_panel[i.bottom_panel_index - 1] = i

    def set_panel_index(self, item: Item, index: int):
        for i in self.container:
            if i.bottom_panel_index == index:
                i.bottom_panel_index = item.bottom_panel_index

        if item.bottom_panel_index == index:
            item.bottom_panel_index = 0
        else:
            item.bottom_panel_index = index

        self.update_panel()

    def draw_inventory_panel(self, screen):
        screen.blit(self.ip_image.image, self.ip_rect)
        ip_pos = Vector2(self.ip_rect.x, self.ip_rect.y)
        first_el_pos = ip_pos + Vector2(game_logic.PANEL_ITEMS_OFFSET, game_logic.PANEL_ITEMS_OFFSET)
        for i in range(len(self.inventory_panel)):
            el_pos = first_el_pos + Vector2(i * (game_logic.PANEL_ITEMS_SIZE + game_logic.PANEL_ITEMS_OFFSET), 0)
            item = self.inventory_panel[i]
            if item:
                icon = ImageWrapper(item.icon.path, item.icon.size)
                icon.set_position(el_pos)
                icon.draw(screen)
                count = str(item.count)
                count_pos = (el_pos + Vector2(1, 1) * game_logic.PANEL_ITEMS_SIZE -
                             game_logic.get_text_size(count, game_logic.PANEL_TEXT_SIZE) -
                             Vector2(1, 0) * game_logic.PANEL_TEXT_OFFSET)
                game_logic.print_text(screen, count, count_pos.x, count_pos.y,
                                      game_logic.PANEL_COUNT_COLOR, font_size=game_logic.PANEL_TEXT_SIZE)
            number = str((i + 1) % 10)
            number_pos = el_pos + Vector2(1, 0) * game_logic.PANEL_TEXT_OFFSET
            game_logic.print_text(screen, number, number_pos.x, number_pos.y,
                                  game_logic.PANEL_NUMBER_COLOR, font_size=game_logic.PANEL_TEXT_SIZE)


class ILootable:
    inventory: GameContainer
