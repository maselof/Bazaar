import pygame
import game_logic
from pygame import Vector2
from image_wrapper import ImageWrapper
from idrawable import IDrawable
from weapon import Weapon


class DescriptionWindow(IDrawable):
    bg_pos: Vector2
    size: Vector2
    item: game_logic.Item
    icon_frame: ImageWrapper

    def __init__(self):
        self.size = game_logic.dscw_size
        self.bg_pos = Vector2((game_logic.g_screen_width - self.size.x) // 2, game_logic.inventory_top_offset)
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
            game_logic.print_text(screen, word, pos.x + current_width, pos.y, game_logic.dw_text_color, font_size=font_size)
            current_width += word_size.x + space_size.x

    def draw_stat(self, screen: pygame.Surface, stat_name: str, stat_value: str, pos: Vector2, right_border: int):
        game_logic.print_text(screen, stat_name, pos.x, pos.y, game_logic.dw_text_color, font_size=game_logic.dscw_stats_text_size)
        value = str(stat_value)
        value_pos = Vector2(right_border - game_logic.get_text_size(value, game_logic.dscw_stats_text_size).x, pos.y)
        game_logic.print_text(screen, value, value_pos.x, value_pos.y, game_logic.dw_text_color, font_size=game_logic.dscw_stats_text_size)

    def draw(self, screen: pygame.Surface):
        if not self.item:
            return

        pygame.draw.rect(screen, game_logic.inventory_background_color, pygame.Rect(self.bg_pos.x, self.bg_pos.y,
                                                                                    self.size.x, self.size.y))

        text_name = self.item.name
        text_name_size = game_logic.get_text_size(text_name, game_logic.dw_text_size)
        text_name_pos = self.bg_pos + Vector2((self.size.x - text_name_size.x) // 2, 0)
        game_logic.print_text(screen, text_name, text_name_pos.x, text_name_pos.y, game_logic.dw_text_color, font_size=game_logic.dw_text_size)

        second_layer_size = self.size - Vector2(2 * game_logic.dw_layers_offset, text_name_size.y + game_logic.dw_layers_offset)
        second_layer_pos = self.bg_pos + Vector2(game_logic.dw_layers_offset, text_name_size.y)
        pygame.draw.rect(screen, game_logic.dw_second_layer_color, pygame.Rect(second_layer_pos.x, second_layer_pos.y,
                                                                               second_layer_size.x, second_layer_size.y))

        self.icon_frame.set_position(second_layer_pos)
        self.icon_frame.draw(screen)
        icon = ImageWrapper(surface=self.item.icon.image.copy())
        icon.set_position(second_layer_pos + Vector2(1, 1) * game_logic.dscw_frame_icon_offset)
        icon.draw(screen)

        description = self.item.description
        description_pos = second_layer_pos + Vector2(game_logic.dscw_frame_icon_offset * 2 + game_logic.panel_items_size, 0) + Vector2(1, 1) * game_logic.dscw_description_offset
        max_width = int(second_layer_pos.x + second_layer_size.x - description_pos.x)
        self.draw_description(screen, description, description_pos, max_width, game_logic.dscw_description_text_size)

        stats_pos = second_layer_pos + Vector2(0, game_logic.dscw_frame_icon_offset * 2 + game_logic.panel_items_size) + Vector2(1, 1) * game_logic.dscw_description_offset
        stats_right_border = second_layer_pos.x + second_layer_size.x - game_logic.dscw_description_offset
        symbol_height = game_logic.get_text_size('A', game_logic.dscw_stats_text_size).y

        if isinstance(self.item, Weapon):
            self.draw_stat(screen, 'Damage', str(self.item.damage), stats_pos, stats_right_border)
            stats_pos.y += symbol_height
            self.draw_stat(screen, 'Attack Speed Modifier', str(self.item.attack_speed_modifier), stats_pos, stats_right_border)
            stats_pos.y += symbol_height
            self.draw_stat(screen, 'Range', str(self.item.attack_range), stats_pos, stats_right_border)
            stats_pos.y += symbol_height

        for effect in self.item.effects:
            self.draw_stat(screen, effect.name, str(effect.value), stats_pos, stats_right_border)
            stats_pos.y += symbol_height

        cost_text_pos = second_layer_pos + Vector2(0, second_layer_size.y - symbol_height) + Vector2(1, -1) * game_logic.dscw_description_offset
        game_logic.print_text(screen, 'Value', cost_text_pos.x, cost_text_pos.y, game_logic.dscw_cost_text_color, font_size=game_logic.dscw_stats_text_size)
        cost = str(self.item.cost)
        cost_pos = Vector2(stats_right_border - game_logic.get_text_size(cost, game_logic.dscw_stats_text_size).x, cost_text_pos.y)
        game_logic.print_text(screen, cost, cost_pos.x, cost_pos.y, game_logic.dscw_cost_text_color, font_size=game_logic.dscw_stats_text_size)


class GameContainer(IDrawable):
    container: [game_logic.Item]
    bg_pos: Vector2
    is_open: bool
    show_frame: bool
    focus_item_index: int
    description_window: DescriptionWindow

    def __init__(self):
        self.container = []
        self.inv_cell_img = pygame.image.load('res/images/interface/inventory/inv_cell.png')
        self.frame_img = ImageWrapper('res/images/interface/inventory/frame.png')
        self.is_open = False
        self.show_frame = False
        self.focus_item_index = 0
        width, height = self.inv_cell_img.get_size()
        self.inv_cell_rect = pygame.Rect(0, 0, width, height)
        self.bg_pos = Vector2(game_logic.g_screen_width - self.inv_cell_rect.size[0] * game_logic.inventory_columns_count, 0) + \
                      Vector2(-1, 1) * game_logic.inventory_top_offset
        self.priority = game_logic.inventory_priority
        self.description_window = DescriptionWindow()

    def close(self):
        self.is_open = False
        self.show_frame = False

    def open(self):
        self.is_open = True
        self.show_frame = True

    def change_focus_item(self, index: int):
        new_index = self.focus_item_index + index
        print(f'Container len: {len(self.container)}')
        if (new_index < 0) | (new_index >= len(self.container)):
            return
        self.focus_item_index = new_index
        print(f'New focus index: {new_index}')
        if self.get_focus_item():
            print(f'Focus item: {self.get_focus_item().name}')
            if isinstance(self.get_focus_item(), Weapon):
                print(self.get_focus_item().is_equipped)
        else:
            print('Focus item is null')

    def get_item(self, index: int):
        if index < 0 or index >= len(self.container):
            return None
        return self.container[index]

    def get_focus_item(self):
        if self.focus_item_index >= len(self.container):
            return None
        return self.container[self.focus_item_index]

    def add_item(self, item: game_logic.Item, count: int = 1):
        for i in self.container:
            if i.name == item.name:
                if isinstance(item, Weapon) and isinstance(i, Weapon) and item.is_equipped != i.is_equipped:
                    print(item.is_equipped, i.is_equipped)
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

    def remove_item(self, item: game_logic.Item, count: int = 1):
        for i in self.container:
            if i.name == item.name:
                if isinstance(item, Weapon) and isinstance(i, Weapon) and item.is_equipped != i.is_equipped:
                    print(item.is_equipped, i.is_equipped)
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

        raws_count = max(len(self.container) // game_logic.inventory_columns_count + 1,
                         game_logic.inventory_min_raws_count)
        cells_count = raws_count * game_logic.inventory_columns_count

        bg_size = Vector2(self.inv_cell_rect.size[0] * game_logic.inventory_columns_count,
                          self.inv_cell_rect.size[1] * raws_count) + 2 * Vector2(game_logic.inventory_left_cell_offset, game_logic.inventory_left_cell_offset)

        pygame.draw.rect(screen, game_logic.inventory_background_color, pygame.Rect(self.bg_pos, bg_size))

        img_width, img_height = self.inv_cell_rect.size

        for i in range(cells_count):
            pos = self.bg_pos + Vector2(img_width * (i % game_logic.inventory_columns_count) + game_logic.inventory_left_cell_offset,
                                  img_height * (i // game_logic.inventory_columns_count) + game_logic.inventory_left_cell_offset)
            self.inv_cell_rect.x, self.inv_cell_rect.y = pos.x, pos.y
            screen.blit(self.inv_cell_img, self.inv_cell_rect)
            if i < len(self.container):
                el_pos = pos + Vector2(1, 1) * game_logic.inventory_left_cell_offset
                self.container[i].icon.set_position(el_pos)
                self.container[i].icon.draw(screen)

                count = str(self.container[i].count)
                count_text_size = game_logic.get_text_size(count, game_logic.inventory_text_size)
                item_icon_size = Vector2(1, 1) * game_logic.panel_items_size
                count_text_pos = el_pos + item_icon_size - count_text_size
                game_logic.print_text(screen, count, count_text_pos.x, count_text_pos.y, game_logic.panel_count_color, font_size=game_logic.inventory_text_size)

                bpi = self.container[i].bottom_panel_index
                if bpi > 0:
                    game_logic.print_text(screen, str(bpi), el_pos.x, el_pos.y, game_logic.panel_number_color, font_size=game_logic.inventory_text_size)

        if self.show_frame:
            cell_size = Vector2(self.inv_cell_rect.size[0])
            frame_pos = self.bg_pos + Vector2(1, 1) * game_logic.inventory_left_cell_offset + Vector2((self.focus_item_index % 5) * cell_size.x,
                                                                                                      (self.focus_item_index // 5) * cell_size.y)
            self.frame_img.set_position(frame_pos)
            self.frame_img.draw(screen)

        if not self.show_frame:
            self.description_window.item = None
        else:
            self.description_window.item = self.get_focus_item()

        self.description_window.draw(screen)


class HeroInventory(GameContainer):
    inventory_panel = [game_logic.Item]

    def __init__(self):
        super().__init__()
        self.inventory_panel = [None for i in range(game_logic.panel_items_count)]
        self.ip_image = pygame.image.load('res/images/interface/inventory/items_panel.png')
        ip_w, ip_h = self.ip_image.get_size()
        self.ip_rect = pygame.Rect((game_logic.g_screen_width - ip_w) // 2,
                                   game_logic.g_screen_height - ip_h - game_logic.panel_bottom_offset, 0, 0)
        self.bg_pos = Vector2(game_logic.inventory_top_offset, game_logic.inventory_top_offset)

    def update(self):
        super().update()
        for i in range(len(self.inventory_panel)):
            if self.inventory_panel[i] and self.inventory_panel[i].count == 0:
                self.inventory_panel[i] = None

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        self.draw_inventory_panel(screen)

    def update_panel(self):
        self.inventory_panel = [None for i in range(game_logic.panel_items_count)]
        for i in self.container:
            print(i.name, i.bottom_panel_index, i.count)
            if i.bottom_panel_index > 0 and i.count > 0:
                self.inventory_panel[i.bottom_panel_index - 1] = i

    def set_panel_index(self, item: game_logic.Item, index: int):
        for i in self.container:
            if i.bottom_panel_index == index:
                i.bottom_panel_index = item.bottom_panel_index

        if item.bottom_panel_index == index:
            item.bottom_panel_index = 0
        else:
            item.bottom_panel_index = index

        self.update_panel()

    def draw_inventory_panel(self, screen):
        screen.blit(self.ip_image, self.ip_rect)
        ip_pos = Vector2(self.ip_rect.x, self.ip_rect.y)
        first_el_pos = ip_pos + Vector2(game_logic.panel_items_offset, game_logic.panel_items_offset)
        for i in range(len(self.inventory_panel)):
            el_pos = first_el_pos + Vector2(i * (game_logic.panel_items_size + game_logic.panel_items_offset), 0)
            item = self.inventory_panel[i]
            if item:
                icon = ImageWrapper(surface=item.icon.image.copy())
                icon.set_position(el_pos)
                icon.draw(screen)
                count = str(item.count)
                count_pos = el_pos + Vector2(1, 1) * game_logic.panel_items_size - game_logic.get_text_size(count, game_logic.panel_text_size) - Vector2(1, 0) * game_logic.panel_text_offset
                game_logic.print_text(screen, count, count_pos.x, count_pos.y, game_logic.panel_count_color, font_size=game_logic.panel_text_size)
            number = str((i + 1) % 10)
            number_pos = el_pos + Vector2(1, 0) * game_logic.panel_text_offset
            game_logic.print_text(screen, number, number_pos.x, number_pos.y, game_logic.panel_number_color, font_size=game_logic.panel_text_size)


class ILootable:
    inventory: GameContainer
