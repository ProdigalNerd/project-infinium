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
from rich.panel import Panel

class Player(Character, HasPersistence, HealthBar, HasExperience):
    class ViewManager:
        def __init__(self):
            self.subscribers = {}
            self.active_view = None
            self.active_callback = None
        def subscribe(self, attribute, callback, view_name):
            if attribute not in self.subscribers:
                self.subscribers[attribute] = {}
            self.subscribers[attribute][view_name] = callback
        def set_active_view(self, view_name, callback):
            self.active_view = view_name
            self.active_callback = callback
        def notify(self, attribute):
            if attribute in self.subscribers and self.active_view in self.subscribers[attribute]:
                self.subscribers[attribute][self.active_view]()
            elif self.active_callback:
                self.active_callback()

    def __init__(self):
        HasPersistence.__init__(self, "./game/data/player.yaml")

        self.inventory = Inventory()
        self.ui_manager = UIManager()
        self.current_location = LocationManager().get_location_by_id(1)  # Assuming starting location is ID 1
        self.command_registry = CommandRegistry()
        self.profession_registry = ProfessionRegistry(self)
        self.event_log = []  # Add a simple event log
        self.view_manager = self.ViewManager()
        # Subscribe views to attributes, but only one will be active at a time
        self.view_manager.subscribe('location', self.show_map, 'show_map')
        self.view_manager.subscribe('event_log', self.event_log_view, 'event_log_view')

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
        self.command_registry.register("event_log", "Show the event log", self.event_log_view)

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
        self.view_manager.notify('location')
        
        self.log_event(f'You traveled to {self.current_location.name}')
        self.view_manager.notify('event_log')

    def get_current_location(self):
        return self.current_location

    def search_current_location(self):
        output, summary = self.current_location.search() # type: ignore
        # Set the active view to the search_current_location view and update the game content
        self.view_manager.set_active_view('search_current_location', lambda: self.ui_manager.update_game_content(output))
        if summary:
            self.log_event(summary)
        self.view_manager.notify('event_log')
    
    def show_map(self):
        self.view_manager.set_active_view('show_map', self.show_map)
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
                self.log_event(f'You moved {direction_to_move.name} towards {self.current_location.name}')
                self.view_manager.notify('location')
                self.view_manager.notify('event_log')
        self.render_player_info()

    def can_visit_shops(self):
        if isinstance(self.current_location, HasShops):
            return len(self.current_location.shops) > 0
        return False
    
    def visit_shop(self):
        if isinstance(self.current_location, HasShops):
            self.current_location.visit_shop(self.ui_manager)

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
            item = self.current_location.visiting_shop.get_item_to_purchase(self.ui_manager)

            output = Text()

            if item:
                if self.currency >= item.cost:
                    self.currency -= item.cost
                    self.inventory.add_item(item)
                    output.append(f"Purchased {item.name} for {item.cost} gold.")
                else:
                    output.append("You don't have enough currency to purchase this item.")
            else:
                output.append("No item selected.")
                
            self.ui_manager.update_game_content(output)
    
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

    def event_log_view(self):
        self.view_manager.set_active_view('event_log_view', self.event_log_view)
        # Recent events (last 5)
        events = self.event_log[-5:] if self.event_log else ["No recent events."]
        events_text = '\n'.join(f"- {event}" for event in events)
        table = Table.grid(expand=True)
        table.add_row(Panel(events_text, title="Recent Events", border_style="magenta"))
        self.ui_manager.update_game_content(table)

    def log_event(self, message: str):
        self.event_log.append(message)
        if len(self.event_log) > 20:
            self.event_log = self.event_log[-20:]
        self.view_manager.notify('event_log')
