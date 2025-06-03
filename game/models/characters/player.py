from console.command_registry import CommandRegistry
from console.ui_manager import UIManager
from game.components.has_experience import HasExperience
from game.components.has_persistence import HasPersistence
from game.components.has_shops import HasShops
from game.components.health import HealthBar
from game.database.models.character import Character
from game.enums.direction import Direction
from game.managers.location_manager import LocationManager
from game.models.inventory.inventory import Inventory
from game.models.inventory.inventory_item import InventoryItem
from game.models.items.base_item import BaseItem
from game.models.skills.profession_registry import ProfessionRegistry
from rich.table import Table
from rich.text import Text

class Player(Character, HasPersistence, HealthBar, HasExperience):
    def __init__(self):
        HasPersistence.__init__(self, "./game/data/player.yaml")

        self.inventory = Inventory()
        self.ui_manager = UIManager()
        self.current_location = LocationManager().get_location_by_id(1)  # Assuming starting location is ID 1
        self.command_registry = CommandRegistry()
        self.profession_registry = ProfessionRegistry(self)

        player_data = self.load_data()
        # Load player data from persistence or initialize with default values
        if player_data:
            self.name = player_data.get("name", "Player")
            self.currency = player_data.get("currency", 100)
            self.strength = player_data.get("strength", 10)
            self.intelligence = player_data.get("intelligence", 10)
            self.agility = player_data.get("agility", 10)

            level = player_data.get("level", 1)
            experience = player_data.get("experience", 0)
            experience_to_next_level = player_data.get("experience_to_next_level", 100)
            HasExperience.__init__(self, experience, level, experience_to_next_level)

            health = player_data.get("max_health", 100)
            current_health = player_data.get("current_health", health)
            HealthBar.__init__(self, current_health, health)

            inventory = player_data.get("inventory", {})
            inventory_items = inventory.get("items", [])
            for item in inventory_items:
                self.inventory.add_item(InventoryItem(
                    item_id=item.get("item_id"),
                    item=BaseItem(name=item.get("name"), cost=item.get("cost")),
                    quantity=item.get("quantity", 1),
                    stackable=item.get("stackable", True)
                ))
        else:
            HealthBar.__init__(self, 100, 100)
            HasExperience.__init__(self)
            self.name = "Player"
            self.strength = 10
            self.intelligence = 10
            self.agility = 10
            self.currency = 100

        self.initialize_commands()
        self.render_player_info()
        self.display_stats()

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

    def render_player_info(self):
        text = Text(
            f"Player: {self.name} | Level: {self.level} | Location: {self.current_location.name if self.current_location else 'None'}",
            style="bold green",
            justify="center"
        )
        self.ui_manager.update_player(text)

    def display_stats(self):
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column("Attribute", style="dim")
        table.add_column("Value", justify="right")

        table.add_row("Health", f"{self.current_health}/{self.max_health}")
        table.add_row("Experience", f"{self.experience}/{self.experience_to_next_level}")
        table.add_row("Strength", str(self.strength))
        table.add_row("Intelligence", str(self.intelligence))
        table.add_row("Agility", str(self.agility))
        table.add_row("Currency", f"{self.currency} gold")

        self.ui_manager.update_player_stats(table)

    def set_name(self, name):
        self.name = name
        self.render_player_info()

    def travel_to_location(self, location_name):
        location_manager = LocationManager()
        self.current_location = location_manager.get_location_by_name(location_name)

    def get_current_location(self):
        return self.current_location

    def search_current_location(self):
        description = self.current_location.search() # type: ignore
        self.ui_manager.update_game_content(description)
    
    def show_map(self):
        location_manager = LocationManager()
        map = location_manager.generate_map()
        self.ui_manager.update_game_content(map)
    
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
        self.render_player_info()

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
