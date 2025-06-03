from console.command_registry import CommandRegistry
from game.managers.location_manager import LocationManager
from game.models.characters.player import Player

class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.player = Player()
            self.location_manager = LocationManager()
            self.command_registry = CommandRegistry()
            self.command_registry.register("create_character", "Create New Character", self.create_character, self.can_create_character)

    def can_create_character(self):
        return not self.player.name != "Player"

    def create_character(self):
        name = input("Enter character name: ")
        self.player.set_name(name)
