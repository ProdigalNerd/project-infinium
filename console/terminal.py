import os

from console.command_registry import CommandRegistry
from console.game_manager import GameManager
from console.ui_manager import UIManager

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
            self.ui_manager = UIManager()
            self.clear_screen()
            self.game_manager.create_character()
            self.initialize_commands()
            self.ui_manager.render()

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

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exit(self):
        print("Exiting the terminal. Goodbye!")
        self.continue_running = False

    def help(self):
        print("Available commands:")
        self.command_registry.list_commands()

    def run(self):
        while self.continue_running:
            print("What would you like to do? Type 'help' for a list of commands.")
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

            self.ui_manager.render()
