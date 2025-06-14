from game.enums.direction import Direction
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
    
    def long_description(self):
        return f'{self.name} is a {self.type.value}. {self.description}'
    
    def direction_from_location(self, other_coordinates):
        """
        Calculate the direction from this location to another location based on coordinates.
        Returns a string indicating the direction.
        """
        dx = other_coordinates[0] - self.coordinates[0]
        dy = other_coordinates[1] - self.coordinates[1]

        if dx > 0:
            x_direction = Direction.EAST.value
        elif dx < 0:
            x_direction = Direction.WEST.value
        else:
            x_direction = ""

        if dy > 0:
            y_direction = Direction.NORTH.value
        elif dy < 0:
            y_direction = Direction.SOUTH.value
        else:
            y_direction = ""

        if x_direction and y_direction:
            return f"{y_direction} {x_direction}"
        elif x_direction:
            return x_direction
        elif y_direction:
            return y_direction
        else:
            return "same location"
    
    def search(self):
        output = Text(f'You search {self.name} but find nothing of interest.', style="dim")
        summary = f'You searched {self.name} but found nothing of interest.'
        return output, summary