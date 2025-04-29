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

    def get_terminal_commands(self):
        commands = [
            ("create_character", self.create_character, True),
        ]
        commands.extend(self.location_manager.get_terminal_commands())
        if self.player:
            commands.extend(self.player.get_terminal_commands())
        if self.player and hasattr(self.player.currentLocation, 'enemies') and len(self.player.currentLocation.enemies) > 0: # type: ignore
            commands.extend(self.player.get_combat_terminal_commands()) # type: ignore
        return commands

    def create_character(self):
        name = input("Enter character name: ")
        self.player = Player(name)
        print(f"Character '{name}' created!")
