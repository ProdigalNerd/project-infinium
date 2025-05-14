from console.command_registry import CommandRegistry
from game.components.has_persistence import HasPersistence
from game.factories.location_abstract_factory import LocationAbstractFactory
from game.enums.location_type import LocationType
from game.generators.random_location import RandomLocation
from game.models.maps.map import Map

class LocationManager(HasPersistence):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocationManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            HasPersistence.__init__(self, "./game/data/locations.yaml")
            self.locations = []
            location_data = self.load_data()
            location_af = LocationAbstractFactory()
            if location_data is not None:
                for location in location_data:
                    self.locations.append(location_af.create_location(LocationType(location["type"]), **location))

            self.current_location = None
            self.command_registry = CommandRegistry()
            self.initialize_commands()

    def initialize_commands(self):
        self.command_registry.register(
            "show_locations",
            "Show available locations",
            self.show_locations
        )
    
    def get_location_by_name(self, name):
        for location in self.locations:
            if location.name.lower() == name.lower():
                return location
        print(f"Location '{name}' not found.")
        return None
    
    def get_location_by_id(self, id):
        for location in self.locations:
            if location.id == id:
                return location
        print(f"Location with ID '{id}' not found.")
        return None

    def add_location(self, location):
        self.locations[location.id] = location
    
    def show_locations(self):
        if not self.locations:
            print("No locations available.")
            return
        print("Available locations:")
        for location in self.locations:
            location.describe()

    def generate_map(self):
        map_generator = Map(self.locations)
        map_generator.generate_map()

    def get_location_by_coordinates(self, coordinates):
        for location in self.locations:
            if location.coordinates == coordinates:
                return location
        print("You have discovered a new location!")
        
        location_generator = RandomLocation(coordinates[0], coordinates[1])
        neighbor_types = self.get_locatin_neighbor_types(coordinates)
        new_location = location_generator.build(neighbor_types, id=len(self.locations) + 1)
        self.save_new_location(new_location)
        self.locations.append(new_location)

        return new_location
    
    def get_locatin_neighbor_types(self, coordinates):
        neighbor_types = []
        for location in self.locations:
            if abs(location.coordinates[0] - coordinates[0]) == 1 and location.coordinates[1] == coordinates[1]:
                neighbor_types.append(location.type)
            elif abs(location.coordinates[1] - coordinates[1]) == 1 and location.coordinates[0] == coordinates[0]:
                neighbor_types.append(location.type)
        return neighbor_types

    def save_new_location(self, location):
        self.save_data(location)