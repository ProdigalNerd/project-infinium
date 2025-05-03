from console.decorators.register_command import register_command
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
            self.player = None
            self.location_manager = LocationManager()

    @register_command("create_character", "Creates a new character.", is_available_fn=lambda self: self.can_create_character())
    def create_character(self):
        name = input("Enter character name: ")
        self.player = Player(name)
        print(f"Character '{name}' created!")

    def can_create_character(self):
        return self.player is None
