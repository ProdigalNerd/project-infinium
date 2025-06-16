import os
import yaml
from ai_game_master.locations import AI_Locations
from game.enums.location_type import LocationType
from game.factories.location_abstract_factory import LocationAbstractFactory
from game.generators.configurations.location_type_config import LOCATION_TYPE_CONFIG
from typing import List
import random

from game.models.locations.base_location import BaseLocation

TEMPLATES = {}

try:
    with open("./game/data/location_templates.yaml", "r") as file:
        TEMPLATES = yaml.safe_load(file)
except FileNotFoundError:
    print("Location templates file not found.")
except yaml.YAMLError as e:
    print(f"Error reading location templates file: {e}")

class RandomLocation:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def build(self, neighboringLocations: List[BaseLocation], id: int = 0):
        neighboringTypes = [location.type for location in neighboringLocations]
        type = self.__get_type__(neighboringTypes)

        matching_location = next((location for location in neighboringLocations if location.type == type), None)
        if matching_location:
            matching_location.coordinates = (self.x, self.y)
            matching_location.id = id if id != 0 else random.randint(1, 1000)
            return matching_location

        ai_location = AI_Locations(api_key=os.getenv("OPENAI_API_KEY"))

        generated_location = ai_location.describe_location(
            location_type=type,
            neighbor_locations=neighboringLocations
        )

        location = {
            'id': id if id != 0 else random.randint(1, 1000),
            'coordinates': {"x": self.x, "y": self.y},
            'type': type.value,
        }

        location.update(generated_location)

        location_factory = LocationAbstractFactory()
        location = location_factory.create_location(type, **location)
        return location

    def __get_type__(self, neighboringTypes: List[LocationType]) -> LocationType:
        available_types = set()
        for type in neighboringTypes:
            available_types.update(LOCATION_TYPE_CONFIG[type])
        available_types = list(available_types)

        return random.choice(available_types) if available_types else LocationType.PLAINS
    
    def __generate_name__(self, location_type: LocationType):
        templates = TEMPLATES[location_type.name]
        name_template = random.choice(templates["names"])
        adjective = random.choice(templates["adjectives"])
        noun = random.choice(templates["nouns"])
        return name_template.format(adjective=adjective, noun=noun)

    def __generate_description__(self, location_type: LocationType):
        templates = TEMPLATES[location_type.name]
        description_template = random.choice(templates["descriptions"])
        adjective = random.choice(templates["adjectives"])
        feature = random.choice(templates["features"])
        return description_template.format(adjective=adjective, feature=feature)
        