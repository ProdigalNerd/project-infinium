from openai import OpenAI
from game.enums.location_type import LocationType
from game.models.locations.base_location import BaseLocation
from pydantic import BaseModel
from typing import List


class Owner(BaseModel):
    name: str
    description: str
    greeting: str

class Shop(BaseModel):
    name: str
    description: str
    types_of_items: str
    owner: Owner

class LocationJsonSchema(BaseModel):
    name: str
    description: str
    shops: List[Shop]

class AI_Locations:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def build_system_prompt(self):
        return {
            "role": "developer",
            "content": "You are an AI game master for a text based role playing game. The game has a fantasy setting, in a world filled with many races. With this being a text based game, descriptions are extremely important."
        }
    
    def build_context(
            self,
            neighbor_locations: list[BaseLocation]):
        context = ""
        for location in neighbor_locations:
            context += f"To the {location.direction_from_location} is {location.long_description()}\n"

        return {
            "role": "developer",
            "content": context
        }
    
    def build_user_prompt(self, location_type: LocationType):
        return {
            "role": "user",
            "content": f"You are currently in a {location_type.value}. Describe the location in detail, including {location_type.define_features()} Use rich, descriptive language to create an immersive experience for the player."
        }

    def describe_location(self, location_type: LocationType, neighbor_locations: list[BaseLocation]):
        response = self.client.responses.parse(
            model="gpt-4o-mini",
            input=[
                self.build_system_prompt(),
                self.build_context(neighbor_locations),
                self.build_user_prompt(location_type)
            ], # type: ignore
            text_format=LocationJsonSchema
        )
        
        return response.output_parsed.model_dump()