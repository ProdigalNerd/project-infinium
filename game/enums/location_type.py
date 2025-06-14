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

    def define_features(self):
        if self.value == "village":
            return "shops with what they sell, and the owner of that shop. Describe the owner and their personality and temperament. Provide the typical greeting they would use when a customer enters their store."
        elif self.value == "plains":
            return "the vast open fields, the flora and fauna, and any notable landmarks. Describe the weather and how it affects the environment. Include any sounds or smells that are characteristic of the plains."
        elif self.value == "forest":
            return "the dense trees, the sounds of wildlife, and any notable landmarks. Describe the weather and how it affects the environment. Include any sounds or smells that are characteristic of the forest. Also include any creatures or monsters that may inhabit the forest, such as goblins, wolves, or bears. Describe their behavior and how they interact with the environment."
        
        return "any unique features, landmarks, or characteristics that define this type of location. Include details about the environment, flora, fauna, and any notable inhabitants or structures."