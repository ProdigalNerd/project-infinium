from console.command_registry import CommandRegistry
from console.ui_manager import UIManager
from game.components.has_experience import HasExperience
from game.components.has_shops import HasShops
from game.components.health import HealthBar
from game.database.models.character import Character
from game.enums.direction import Direction
from game.managers.location_manager import LocationManager
from game.models.inventory.inventory import Inventory
from game.models.skills.profession_registry import ProfessionRegistry

class Player(Character, HealthBar, HasExperience):
    def __init__(self, name: str):
        HealthBar.__init__(self, 100)
        HasExperience.__init__(self)
        self.name = name
        self.strength = 10
        self.intelligence = 10
        self.agility = 10
        self.ui_manager = UIManager()
        self.current_location = LocationManager().get_location_by_id(1)  # Assuming starting location is ID 1
        self.inventory = Inventory()
        self.command_registry = CommandRegistry()
        self.profession_registry = ProfessionRegistry(self)
        self.currency = 100
        self.initialize_commands()

    def initialize_commands(self):
        self.command_registry.register("stats", "Display player stats", self.display_stats)
        self.command_registry.register("travel", "Travel to a location", self.travel_to_location, has_extra_args=True)
        self.command_registry.register("search", "Search the current location", self.search_current_location)
        self.command_registry.register("visit_shop", "Visit a shop in the current location", self.visit_shop, self.can_visit_shops)
        self.command_registry.register("leave_shop", "Leave the shop you are currently visiting", self.leave_shop, self.is_visiting_shop)
        self.command_registry.register("browse_shop", "Browse the items in the shop", self.browse_shop, self.is_visiting_shop)
        self.command_registry.register("purchase_item", "Purchase an item from the shop", self.purchase_item, self.is_visiting_shop)
        self.command_registry.register("sell_item", "Sell an item to the shop", self.sell_item, self.is_visiting_shop)
        self.command_registry.register("map", "Show the map of the current location", self.show_map)
        self.command_registry.register("move", "Move in a direction", self.move_in_direction, has_extra_args=True)
        self.command_registry.register("view_inventory", "View your inventory", self.inventory.list_items)

    def display_stats(self):
        self.ui_manager.render_player_stats(self)

    def travel_to_location(self, location_name):
        location_manager = LocationManager()
        self.current_location = location_manager.get_location_by_name(location_name)

    def get_current_location(self):
        return self.current_location

    def search_current_location(self):
        self.current_location.search() # type: ignore
    
    def show_map(self):
        location_manager = LocationManager()
        location_manager.generate_map()
    
    def move_in_direction(self, direction):
        location_manager = LocationManager()
        if self.current_location:
            direction_to_move = Direction(direction)
            new_coordinates = (
                self.current_location.coordinates[0] + direction_to_move.toTuple()[0],
                self.current_location.coordinates[1] + direction_to_move.toTuple()[1]
            )
            new_location = location_manager.get_location_by_coordinates(new_coordinates)
            if new_location:
                self.current_location = new_location
                print(f"Moved to {self.current_location.name}.")
            else:
                print("You can't go that way.")
        else:
            print("You are not in a location.")

    def can_visit_shops(self):
        if isinstance(self.current_location, HasShops):
            return len(self.current_location.shops) > 0
        return False
    
    def visit_shop(self):
        if isinstance(self.current_location, HasShops):
            self.current_location.visit_shop()

    def is_visiting_shop(self):
        if isinstance(self.current_location, HasShops):
            return self.current_location.visiting_shop is not None
        return False
    
    def leave_shop(self):
        if isinstance(self.current_location, HasShops):
            self.current_location.leave_shop()

    def browse_shop(self):
        if isinstance(self.current_location, HasShops) and self.current_location.visiting_shop:
            self.current_location.visiting_shop.list_items()

    def purchase_item(self):
        if isinstance(self.current_location, HasShops) and self.current_location.visiting_shop:
            item = self.current_location.visiting_shop.get_item_to_purchase()
            if item:
                if self.currency >= item.cost:
                    self.currency -= item.cost
                    self.inventory.add_item(item)
                    print(f"Purchased {item.name} for {item.cost} gold.")
                else:
                    print("You don't have enough currency to purchase this item.")
            else:
                print("No item selected.")
    
    def sell_item(self):
        if isinstance(self.current_location, HasShops) and self.current_location.visiting_shop:
            item = self.inventory.select_item()
            if item:
                self.currency += item.cost // 2
                self.inventory.remove_item(item)

    def add_loot(self, loot):
        if isinstance(loot, list):
            for item in loot:
                self.inventory.add_item(item)
        else:
            self.inventory.add_item(loot)

    def calculate_attack(self):
        return self.strength
