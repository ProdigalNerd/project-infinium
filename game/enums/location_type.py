from enum import Enum

class LocationType(Enum):
    """
    Enum representing different types of locations in the game.
    """
    TOWN = "town"
    CASTLE = "castle"
    VILLAGE = "village"

    FOREST = "forest"
    PLAINS = "plains"
    SWAMP = "swamp"
    MOUNTAIN = "mountain"
    DESERT = "desert"
    OCEAN = "ocean"
    LAKE = "lake"

    RUINS = "ruins"
    DUNGEON = "dungeon"
    CAVE = "cave"