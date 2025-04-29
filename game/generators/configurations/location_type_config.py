from game.enums.location_type import LocationType

LOCATION_TYPE_CONFIG = {
    LocationType.VILLAGE: [
        LocationType.PLAINS,
        LocationType.FOREST
    ],
    LocationType.FOREST: [
        LocationType.FOREST,
        LocationType.PLAINS,
        LocationType.VILLAGE,
    ],
    LocationType.PLAINS: [
        LocationType.FOREST,
        LocationType.VILLAGE,
        LocationType.PLAINS,
    ],
}