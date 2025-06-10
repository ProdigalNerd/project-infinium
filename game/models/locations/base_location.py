from game.enums.location_type import LocationType
from rich.text import Text


class BaseLocation():
    """
    Abstract base class for all locations in the game.
    """

    def __init__(self, location_data):
        self.id = location_data['id']
        self.name = location_data['name']
        self.description = location_data['description']
        self.coordinates = (location_data['coordinates']['x'], location_data['coordinates']['y'])
        self.type = LocationType[location_data['type'].upper()]

    def get_type(self) -> LocationType:
        return self.type

    def enter(self) -> None:
        """
        Abstract method to be implemented by subclasses.
        This method should define what happens when a player enters the location.
        """
        pass

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "coordinates": {"x": self.coordinates[0], "y": self.coordinates[1]}
        }
    
    def __str__(self):
        return f"{self.name} ({self.coordinates}): {self.description}"
    
    def search(self) -> Text:
        """
        Abstract method to be implemented by subclasses.
        This method should define what happens when a player searches the location.
        """
        pass