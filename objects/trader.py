import game_cycle
import game_logic
from chest import *


class Trader(Chest):

    def __init__(self,
                 size: Vector2,
                 collision_rect_offset: Vector2):
        super().__init__('trading_counter', 'buildings/', size, collision_rect_offset)
        game_cycle.add_interface_element(self.inventory)
        self.refresh_wares()

    def sounds_init(self):
        self.sounds = {'Open': SoundWrapper(None, True, 0.1),
                       'Close': SoundWrapper(None, True, 0.1)}

    def refresh_wares(self):
        self.inventory.container.clear()
        for key in game_logic.ITEMS.keys():
            item = game_logic.get_item(key)
            self.inventory.add_item(item, item.trading_count)
