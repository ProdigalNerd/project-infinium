from game.enums.location_type import LocationType
from game.factories.location_abstract_factory import LocationAbstractFactory
from game.generators.configurations.location_type_config import LOCATION_TYPE_CONFIG
from faker import Faker
from typing import List
import random

fake = Faker()

class RandomLocation:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def build(self, neighboringTypes: List[LocationType], id: int = 0):
        type = self.__get_type__(neighboringTypes)
        name = self.__get_name__(type)
        description = self.__get_description__(type)

        location = {
            'id': id if id != 0 else random.randint(1, 1000),
            'name': name,
            'description': description,
            'coordinates': {"x": self.x, "y": self.y},
        }

        location_factory = LocationAbstractFactory()
        location = location_factory.create_location(type, **location)
        return location

    def __get_type__(self, neighboringTypes: List[LocationType]) -> LocationType:
        available_types = set()
        for type in neighboringTypes:
            available_types.update(LOCATION_TYPE_CONFIG[type])
        available_types = list(available_types)

        return random.choice(available_types) if available_types else LocationType.PLAINS
    
    def __get_name__(self, type: LocationType):
        if type == LocationType.VILLAGE:
            return fake.city()
        elif type == LocationType.FOREST:
            return fake.name() + " Forest"
        elif type == LocationType.PLAINS:
            return fake.name() + " Plains"
        else:
            return fake.name()
        
    def __get_description__(self, type: LocationType):
        if type == LocationType.VILLAGE:
            return fake.paragraph()
        elif type == LocationType.FOREST:
            return fake.paragraph()
        elif type == LocationType.PLAINS:
            return fake.paragraph()
        else:
            return fake.paragraph()
        