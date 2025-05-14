from game.models.locations.base_location import BaseLocation
from console.helpers.pad_colored_text import pad_colored_text

from colorama import Fore, Style

class Map:
    def __init__(self, existing_locations: list[BaseLocation] = []):
        self.grid = {}

        if existing_locations is not None:
            for location in existing_locations:
                self.grid[location.coordinates] = location

    def generate_map(self):
        if not self.grid:
            print("No locations available.")
            return

        # Determine the bounds of the grid
        min_x = min(coordinate[0] for coordinate in self.grid.keys())
        max_x = max(coordinate[0] for coordinate in self.grid.keys())
        min_y = min(coordinate[1] for coordinate in self.grid.keys())
        max_y = max(coordinate[1] for coordinate in self.grid.keys())

        # Create a grid representation
        grid = [[" " for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]

        # Populate the grid with location names or markers
        current_location = None  # Define or pass the current location as needed
        for (x, y), location in self.grid.items():
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