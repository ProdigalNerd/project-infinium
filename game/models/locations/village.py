from game.components.has_shops import HasShops
from game.enums.location_type import LocationType
from game.models.locations.base_location import BaseLocation

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
        self.describe()
        if self.shops:
            print("Some shops are available!")
            for shop in self.shops:
                print(f"- {shop.name}")
        else:
            print("The forest is quiet. You find nothing of interest.")
