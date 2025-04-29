from game.enums.location_type import LocationType
from game.models.base_location import BaseLocation

class Plains(BaseLocation):
    def __init__(self, location_data):
        self.id = location_data['id']
        self.name = location_data['name']
        self.description = location_data['description']
        self.coordinates = (location_data['coordinates']['x'], location_data['coordinates']['y'])
        self.type = LocationType.PLAINS

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": LocationType.PLAINS.value,
            "coordinates": {"x": self.coordinates[0], "y": self.coordinates[1]}
        }

    def describe(self):
        print(self)