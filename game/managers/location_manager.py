import yaml
from console.command_registry import CommandRegistry
from console.helpers.pad_colored_text import pad_colored_text
from game.factories.location_abstract_factory import LocationAbstractFactory
from game.enums.location_type import LocationType
from game.generators.random_location import RandomLocation
from colorama import Fore, Style

class LocationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocationManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.locations = []
            try:
                with open("./game/data/locations.yaml", "r") as file:
                    location_data = yaml.safe_load(file)

                    location_af = LocationAbstractFactory()
                    for location in location_data:
                        self.locations.append(location_af.create_location(LocationType(location["type"]), **location))
            except FileNotFoundError:
                print("Locations file not found.")
            except yaml.YAMLError as e:
                print(f"Error reading locations file: {e}")

            self.current_location = None
            self.command_registry = CommandRegistry()
            self.initialize_commands()

    def initialize_commands(self):
        self.command_registry.register(
            "show_locations",
            "Show available locations",
            self.show_locations
        )
    
    def get_location_by_name(self, name):
        for location in self.locations:
            if location.name.lower() == name.lower():
                return location
        print(f"Location '{name}' not found.")
        return None
    
    def get_location_by_id(self, id):
        for location in self.locations:
            if location.id == id:
                return location
        print(f"Location with ID '{id}' not found.")
        return None

    def add_location(self, location):
        self.locations[location.id] = location
    
    def show_locations(self):
        if not self.locations:
            print("No locations available.")
            return
        print("Available locations:")
        for location in self.locations:
            location.describe()
    
    def generate_map(self, current_location):
        if not self.locations:
            print("No locations available.")
            return

        # Determine the bounds of the grid
        min_x = min(location.coordinates[0] for location in self.locations)
        max_x = max(location.coordinates[0] for location in self.locations)
        min_y = min(location.coordinates[1] for location in self.locations)
        max_y = max(location.coordinates[1] for location in self.locations)

        # Create a grid representation
        grid = [[" " for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]

        # Populate the grid with location names or markers
        for location in self.locations:
            x, y = location.coordinates
            if current_location and location.id == current_location.id:  # Highlight the current location
                grid[y - min_y][x - min_x] = Fore.GREEN + location.name[0:5] + Style.RESET_ALL
            else:
                grid[y - min_y][x - min_x] = location.name[0:5]  # Use the first 5 characters of the location name

        # Print the grid
        print("Map of locations:")
        row_separator = "-" * ((max_x - min_x + 1) * 12 - 3)  # Adjust length for cell width and separators
        for i, row in enumerate(reversed(grid)):  # Reverse rows to display correctly in Cartesian coordinates
            print(" | ".join(pad_colored_text(cell, 10) for cell in row))  # Print the row
            if i < len(grid) - 1:  # Add a separator after each row except the last one
                print(row_separator)

    def get_location_by_coordinates(self, coordinates):
        for location in self.locations:
            if location.coordinates == coordinates:
                return location
        print("You have discovered a new location!")
        
        location_generator = RandomLocation(coordinates[0], coordinates[1])
        neighbor_types = self.get_locatin_neighbor_types(coordinates)
        new_location = location_generator.build(neighbor_types, id=len(self.locations) + 1)
        self.save_new_location(new_location)
        self.locations.append(new_location)

        return new_location
    
    def get_locatin_neighbor_types(self, coordinates):
        neighbor_types = []
        for location in self.locations:
            if abs(location.coordinates[0] - coordinates[0]) == 1 and location.coordinates[1] == coordinates[1]:
                neighbor_types.append(location.type)
            elif abs(location.coordinates[1] - coordinates[1]) == 1 and location.coordinates[0] == coordinates[0]:
                neighbor_types.append(location.type)
        return neighbor_types

    def save_new_location(self, location):
        try:
            with open("./game/data/locations.yaml", "a") as file:
                yaml.dump([location.toDict()], file, sort_keys=False)
        except FileNotFoundError:
            print("Locations file not found.")
        except yaml.YAMLError as e:
            print(f"Error writing to locations file: {e}")