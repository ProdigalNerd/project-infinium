from enum import Enum

class Direction(Enum):
    """
    Enum representing the four cardinal directions.
    """
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    def __str__(self):
        return self.value.capitalize()
    
    def toTuple(self):
        """
        Convert the direction to a tuple representation.
        """
        direction_coordinates = {
            Direction.NORTH.value: (0, 1),
            Direction.SOUTH.value: (0, -1),
            Direction.EAST.value: (1, 0),
            Direction.WEST.value: (-1, 0)
        }
        return direction_coordinates.get(self.value, (0, 0))
    