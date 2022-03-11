from interface import *
import interface
import game_logic
from pygame import Vector2


class GameContainer:
    container = [game_logic.Item]
    bg_pos: Vector2

    def __init__(self):
        self.container = [game_logic.get_item(0), game_logic.get_item(2)]
        self.inv_cell_img = pygame.image.load('res/images/interface/inventory/inv_cell.png')
        width, height = self.inv_cell_img.get_size()
        self.inv_cell_rect = pygame.Rect(0, 0, width, height)
        self.bg_pos = Vector2(game_logic.g_screen_width - self.inv_cell_rect.size[0] * game_logic.inventory_columns_count, 0) + \
                      Vector2(-1, 1) * game_logic.inventory_top_offset

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        if not game_logic.draw_inventory:
            return

        raws_count = max(len(self.container) // game_logic.inventory_columns_count + 1,
                         game_logic.inventory_min_raws_count)
        cells_count = raws_count * game_logic.inventory_columns_count

        bg_size = Vector2(self.inv_cell_rect.size[0] * game_logic.inventory_columns_count,
                          self.inv_cell_rect.size[1] * raws_count) + 2 * Vector2(game_logic.inventory_left_cell_offset, game_logic.inventory_left_cell_offset)

        pygame.draw.rect(screen, (129, 81, 54), pygame.Rect(self.bg_pos, bg_size))

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


class HeroInventory(GameContainer):
    inventory_panel = [game_logic.Item]

    def __init__(self):
        super().__init__()
        self.inventory_panel = [game_logic.get_item(0), game_logic.get_item(2)]
        self.ip_image = pygame.image.load('res/images/interface/inventory/items_panel.png')
        ip_w, ip_h = self.ip_image.get_size()
        self.ip_rect = pygame.Rect((game_logic.g_screen_width - ip_w) // 2,
                                   game_logic.g_screen_height - ip_h - game_logic.panel_bottom_offset, 0, 0)
        self.bg_pos = Vector2(game_logic.inventory_top_offset, game_logic.inventory_top_offset)

    def draw_inventory_panel(self, screen):
        screen.blit(self.ip_image, self.ip_rect)
        ip_pos = Vector2(self.ip_rect.x, self.ip_rect.y)
        first_el_pos = ip_pos + Vector2(game_logic.panel_items_offset, game_logic.panel_items_offset)
        for i in range(len(self.inventory_panel)):
            el_pos = first_el_pos + Vector2(i * (game_logic.panel_items_size + game_logic.panel_items_offset), 0)
            self.inventory_panel[i].icon.set_position(el_pos)
            self.inventory_panel[i].icon.draw(screen)


