from game.enums.location_type import LocationType


class LocationAbstractFactory:
    """
    Abstract factory for creating locations.
    """

    def __init__(self):
        self.creators = {
            LocationType.VILLAGE.value: self.__create_village__,
            LocationType.FOREST.value: self.__create_forest__,
            LocationType.PLAINS.value: self.__create_plains__,
        }

    def create_location(self, location_type: LocationType, *args, **kwargs):
        """
        Create a location based on the provided location type.
        """
        creator = self.creators.get(location_type.value)
        if not creator:
            raise ValueError(f"Unknown location type: {location_type.value}")
        return creator(*args, **kwargs)
    
    def __create_village__(self, *args, **kwargs):
        from game.models.locations.village import Village
        return Village(kwargs)
    
    def __create_forest__(self, *args, **kwargs):
        from game.models.locations.forest import Forest
        return Forest(kwargs)

    def __create_plains__(self, *args, **kwargs):
        from game.models.locations.plains import Plains
        return Plains(kwargs)