from game.models.locations.base_location import BaseLocation
from colorama import Fore, Style
from rich.table import Table

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
        table = Table(show_header=False, box=None, padding=(0, 1))

        # Add rows to the table
        for row in reversed(grid):  # Reverse rows to display correctly in Cartesian coordinates
            table.add_row(*row)

        return table