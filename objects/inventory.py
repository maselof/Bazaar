from interface import *
import interface
import game_logic
from pygame import Vector2
from image_wrapper import ImageWrapper
from idrawable import IDrawable


class GameContainer(IDrawable):
    container = [game_logic.Item]
    bg_pos: Vector2
    show: bool
    show_frame: bool
    focus_item_index: int

    def __init__(self):
        self.container = []
        self.inv_cell_img = pygame.image.load('res/images/interface/inventory/inv_cell.png')
        self.frame_img = ImageWrapper('res/images/interface/inventory/frame.png')
        self.show = False
        self.show_frame = False
        self.focus_item_index = 0
        width, height = self.inv_cell_img.get_size()
        self.inv_cell_rect = pygame.Rect(0, 0, width, height)
        self.bg_pos = Vector2(game_logic.g_screen_width - self.inv_cell_rect.size[0] * game_logic.inventory_columns_count, 0) + \
                      Vector2(-1, 1) * game_logic.inventory_top_offset
        self.priority = game_logic.inventory_priority

    def change_focus_item(self, index: int):
        new_index = self.focus_item_index + index
        print(len(self.container))
        if (new_index < 0) | (new_index >= len(self.container)):
            return
        self.focus_item_index = new_index
        print(new_index)

    def add_item(self, item: game_logic.Item):
        for i in self.container:
            if i.name == item.name:
                i.count += item.count
                return
        self.container.append(item)

    def remove_item(self, item: game_logic.Item, count: int):
        for i in self.container:
            if i.name == item.name:
                i.count = max(0, i.count - count)

    def update(self):
        for item in self.container:
            if item.count <= 0:
                self.container.remove(item)

    def draw(self, screen: pygame.Surface):
        if not self.show:
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

                message = str(self.container[i].count)
                count_text_size = interface.get_text_size(message, game_logic.inventory_text_size)
                item_icon_size = Vector2(1, 1) * game_logic.panel_items_size
                count_text_pos = el_pos + item_icon_size - count_text_size
                interface.print_text(screen, message, count_text_pos.x, count_text_pos.y, font_size=game_logic.inventory_text_size)

        if self.show_frame:
            cell_size = Vector2(self.inv_cell_rect.size[0])
            frame_pos = self.bg_pos + Vector2(1, 1) * game_logic.inventory_left_cell_offset + Vector2((self.focus_item_index % 5) * cell_size.x,
                                                                                                      (self.focus_item_index // 5) * cell_size.y)
            self.frame_img.set_position(frame_pos)
            self.frame_img.draw(screen)


class HeroInventory(GameContainer):
    inventory_panel = [game_logic.Item]

    def __init__(self):
        super().__init__()
        self.inventory_panel = []
        self.ip_image = pygame.image.load('res/images/interface/inventory/items_panel.png')
        ip_w, ip_h = self.ip_image.get_size()
        self.ip_rect = pygame.Rect((game_logic.g_screen_width - ip_w) // 2,
                                   game_logic.g_screen_height - ip_h - game_logic.panel_bottom_offset, 0, 0)
        self.bg_pos = Vector2(game_logic.inventory_top_offset, game_logic.inventory_top_offset)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        self.draw_inventory_panel(screen)

    def draw_inventory_panel(self, screen):
        screen.blit(self.ip_image, self.ip_rect)
        ip_pos = Vector2(self.ip_rect.x, self.ip_rect.y)
        first_el_pos = ip_pos + Vector2(game_logic.panel_items_offset, game_logic.panel_items_offset)
        for i in range(len(self.inventory_panel)):
            el_pos = first_el_pos + Vector2(i * (game_logic.panel_items_size + game_logic.panel_items_offset), 0)
            self.inventory_panel[i].icon.set_position(el_pos)
            self.inventory_panel[i].icon.draw(screen)


