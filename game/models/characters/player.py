from tabulate import tabulate
from console.command_registry import CommandRegistry
from game.components.health import HealthBar
from game.database.models.character import Character
from game.enums.direction import Direction
from game.managers.combat_manager import CombatManager
from game.managers.location_manager import LocationManager
from game.models.inventory.inventory import Inventory

class Player(Character, HealthBar):
    def __init__(self, name: str):
        HealthBar.__init__(self, 100)
        self.name = name
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.strength = 10
        self.intelligence = 10
        self.agility = 10
        self.currentLocation = LocationManager().get_location_by_id(1)  # Assuming starting location is ID 1
        self.inventory = Inventory()
        self.command_registry = CommandRegistry()
        self.initialize_commands()

    def initialize_commands(self):
        self.command_registry.register("stats", "Display player stats", self.display_stats)
        self.command_registry.register("travel", "Travel to a location", self.travel_to_location)
        self.command_registry.register("search", "Search the current location", self.search_current_location)
        self.command_registry.register("map", "Show the map of the current location", self.show_map)
        self.command_registry.register("move", "Move in a direction", self.move_in_direction)
        self.command_registry.register("fight", "Fight an enemy in the current location", self.fight)

    def display_stats(self):
        stats = [
            ["Name", self.name],
            ["Location", self.currentLocation.name if self.currentLocation else "None"],
            ["Level", self.level],
            ["Health", f"{self.current_health}/{self.max_health}"],
            ["Experience", f"{self.experience}/{self.experience_to_next_level}"],
            ["Strength", self.strength],
            ["Intelligence", self.intelligence],
            ["Agility", self.agility]
        ]
        print(tabulate(stats, headers=["Attribute", "Value"], tablefmt="grid"))

    def travel_to_location(self, location_name):
        location_manager = LocationManager()
        self.currentLocation = location_manager.get_location_by_name(location_name)

    def search_current_location(self):
        self.currentLocation.search() # type: ignore
    
    def show_map(self):
        location_manager = LocationManager()
        location_manager.generate_map(self.currentLocation)
    
    def move_in_direction(self, direction):
        location_manager = LocationManager()
        if self.currentLocation:
            direction_to_move = Direction(direction)
            new_coordinates = (
                self.currentLocation.coordinates[0] + direction_to_move.toTuple()[0],
                self.currentLocation.coordinates[1] + direction_to_move.toTuple()[1]
            )
            new_location = location_manager.get_location_by_coordinates(new_coordinates)
            if new_location:
                self.currentLocation = new_location
                print(f"Moved to {self.currentLocation.name}.")
            else:
                print("You can't go that way.")
        else:
            print("You are not in a location.")

    def add_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            print("You leveled up!")

    def add_loot(self, loot):
        if isinstance(loot, list):
            for item in loot:
                self.inventory.add_item(item)
        else:
            self.inventory.add_item(loot)

    def calculate_attack(self):
        return self.strength

    def fight(self):
        if self.currentLocation and len(self.currentLocation.enemies) > 0:
            enemy = self.currentLocation.enemies.pop(0)
            print(f"You are fighting a {type(enemy).__name__}.")

            combat_manager = CombatManager()
            combat_manager.initialize_combat(self, enemy)
        else:
            print("No enemies to fight.")


