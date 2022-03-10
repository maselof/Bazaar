from interface import *
import interface
import game_logic


class Resource:
    def __init__(self, name, image_path):
        self.name = name
        self.amount = 0
        self.image = pygame.image.load(image_path)


class Inventory:
    whole_inventory = [Resource]

    def __init__(self):
        self.resources = {
            "potion": Resource('potion', "res/animations/objects/potions/heal_potion/idle/icon1.png")
        }
        self.inventory_panel = [None] * 8
        self.whole_inventory = [None] * 8

    def increase(self, name):
        try:
            self.resources[name].amount += 1
            self.update_whole()
            print(self.whole_inventory)
        except KeyError:
            print("Error increasing")

    def get_amount(self, name):
        try:
            return self.resources[name].amount
        except KeyError:
            return -1

    def update_whole(self):
        for name, resource in self.resources.items():
            if resource.amount != 0 and Resource not in self.whole_inventory:
                self.whole_inventory.insert(self.whole_inventory.index(None), resource)
                self.whole_inventory.remove(None)

    def draw_whole(self, screen):
        if not game_logic.draw_inventory:
            return
        x = screen.get_size()[0] // 2 - 780 // 2
        y = screen.get_size()[1] // 2 - 180 // 2
        side = 80
        step = 100
        pygame.draw.rect(screen, (182, 195, 206), (x - 20, y - 20, 820, 220))
        for cell in self.whole_inventory:
            pygame.draw.rect(screen, (200, 215, 227), (x, y, side, side))
            if cell is not None:
                screen.blit(cell.image, (x + 15, y + 5))
                interface.print_text(screen, str(cell.amount), x + 30, y + 60, font_size=15)
            x += step
            if x > screen.get_size()[0] // 2 - 780 // 2 + 700:
                x = screen.get_size()[0] // 2 - 780 // 2
                y += step

    def draw_inventory_panel(self, screen):
        x = screen.get_size()[0] // 2 - 780 // 2
        y = screen.get_size()[1] - 200
        side = 80
        step = 100
        pygame.draw.rect(screen, (182, 195, 206), (x - 20, y - 20, 820, 120))
        for cell in self.inventory_panel:
            pygame.draw.rect(screen, (200, 215, 227), (x, y, side, side))
            x += step
