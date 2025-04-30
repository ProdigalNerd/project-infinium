from typing import Union
from tabulate import tabulate
from game.components.health import HealthBar
from game.database.models.character import Character
from game.enums.direction import Direction
from game.managers.location_manager import LocationManager
from game.models.characters.base_enemy import BaseEnemy


class Player(Character):
    def __init__(self, name: str):
        self.name = name
        self.health = HealthBar(100)
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.strength = 10
        self.intelligence = 10
        self.currentLocation = LocationManager().get_location_by_id(1)  # Assuming starting location is ID 1
        self.combat_target: Union[BaseEnemy, None] = None

    def get_terminal_commands(self):
        commands = [
            ("show_stats", self.display_stats, False),
            ("show_map", self.show_map, False),
            ("travel", self.travel_to_location, False),
            ("explore", self.move_in_direction, False),
            ("search_location", self.search_current_location, False),
        ]
        return commands
    
    def get_combat_terminal_commands(self):
        commands = [
            ("fight", self.fight, False),
        ]
        return commands

    def display_stats(self):
        stats = [
            ["Name", self.name],
            ["Location", self.currentLocation.name if self.currentLocation else "None"],
            ["Level", self.level],
            ["Health", f"{self.health.current}/{self.max}"],
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

    def __calculate_attack__(self):
        return self.strength
    
    def take_damage(self, damage: int):
        self.health.take_damage(damage)

    def fight(self):
        if self.currentLocation and len(self.currentLocation.enemies) > 0:
            self.combat_target = self.currentLocation.enemies.pop(0)
            print(f"You are fighting a {type(self.combat_target).__name__}.")
        
        while self.combat_target and self.health.current > 0:
            player_damage = self.__calculate_attack__()
            self.combat_target.take_damage(player_damage)
            print(f"You dealt {player_damage} damage to the {type(self.combat_target).__name__}.")
            
            if not self.combat_target.is_alive():
                print(f"You defeated the {type(self.combat_target).__name__}!")
                self.add_experience(self.combat_target.get_experience_reward())
                self.combat_target = None
                break

            self.combat_target.attack_player(self)
            print(f"Current health: {self.health.current}/{self.health.max}")
            
            if self.health.current <= 0:
                print("You have died.")
                break


