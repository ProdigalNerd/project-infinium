from console.command_registry import CommandRegistry
from game.enums.location_type import LocationType
from game.models.locations.base_location import BaseLocation
from game.models.shops.base_shop import BaseShop

class Village(BaseLocation):
    def __init__(self, location_data):
        self.id = location_data['id']
        self.name = location_data['name']
        self.description = location_data['description']
        self.coordinates = (location_data['coordinates']['x'], location_data['coordinates']['y'])
        self.type = LocationType.VILLAGE
        self.shops = [BaseShop(shop) for shop in location_data['shops']]

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
        self.describe()
        if self.shops:
            print("Some shops are available!")
            for shop in self.shops:
                print(f"- {shop.name}")
        else:
            print("The forest is quiet. You find nothing of interest.")

    def visit_shop(self):
        if not self.shops:
            print("There are no shops in this village.")
            return

        print("Available shops:")
        for index, shop in enumerate(self.shops, start=1):
            print(f"{index}. {shop.name}")

        try:
            choice = int(input("Enter the number of the shop you want to visit: "))
            if 1 <= choice <= len(self.shops):
                selected_shop = self.shops[choice - 1]
                print(f"You visit {selected_shop.name}.")
                
            else:
                print("Invalid choice. Please select a valid shop number.")
        except ValueError:
            print("Invalid input. Please enter a number.")