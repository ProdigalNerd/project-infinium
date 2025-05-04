import os

from console.command_registry import CommandRegistry
from game.managers.game_manager import GameManager

class Terminal:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Terminal, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.continue_running = True
            self.protected_commands = ["help", "exit", "clear"]
            self.command_registry = CommandRegistry()
            self.game_manager = GameManager()
            self.initialize_commands()

    def initialize_commands(self):
        self.command_registry.register(
            "exit",
            "Exits the terminal.",
            self.exit
        )
        self.command_registry.register(
            "help",
            "Displays available commands.",
            self.help
        )
        self.command_registry.register(
            "clear",
            "Clears the terminal screen.",
            self.clear_screen
        )

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exit(self):
        print("Exiting the terminal. Goodbye!")
        self.continue_running = False

    def help(self):
        print("Available commands:")
        self.command_registry.list_commands()

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the terminal! Type 'help' for a list of commands.")
        while self.continue_running:
            command_input = input("> ").strip().lower()
            parts = command_input.split()
            if not parts:
                continue

            command_name = parts[0]
            args = parts[1:]

            command = self.command_registry.get_command(command_name)
            if command:
                command.execute(self, *args)
            else:
                print(f"Unknown command: {command_name}")
