from enum import Enum

class MapLevel(Enum):
    """
    Enum representing different levels of map hierarchy in the game.
    Each level represents a different scale of location, from specific locations
    to the entire world.
    """
    LOCATION = "location"
    CITY = "city"
    DISTRICT = "district"
    PROVINCE = "province"
    REGION = "region"
    CONTINENT = "continent"
    WORLD = "world"
