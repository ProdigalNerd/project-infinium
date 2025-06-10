from game.components.has_shops import HasShops
from game.enums.location_type import LocationType
from game.models.locations.base_location import BaseLocation
from rich.text import Text


class Village(BaseLocation, HasShops):
    def __init__(self, location_data):
        HasShops.__init__(self, location_data['shops'] if 'shops' in location_data else [])
        self.id = location_data['id']
        self.name = location_data['name']
        self.description = location_data['description']
        self.coordinates = (location_data['coordinates']['x'], location_data['coordinates']['y'])
        self.type = LocationType.VILLAGE

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": LocationType.VILLAGE.value,
            "coordinates": {"x": self.coordinates[0], "y": self.coordinates[1]},
            "shops": self.shops
        }

    def describe(self):
        print(self)

    def search(self):
        output = Text()
        output.append(f"You are in {self.name}.\n", style="bold green")
        output.append(f"{self.coordinates[0]}, {self.coordinates[1]}\n", style="bold cyan")
        output.append(f"{self.description}\n")
        if self.shops:
            output.append("You find some shops in the village:\n", style="bold green")
            for shop in self.shops:
                output.append(f"- {shop.name}\n", style="bold blue")
        else:
            output.append("There are no shops in this village.", style="bold red")

        return output
