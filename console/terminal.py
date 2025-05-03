import os

from console.command_registry import CommandRegistry
from console.decorators.register_command import register_command
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

    @register_command("clear", "Clears the console screen")
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    @register_command("exit", "Exits the terminal")
    def exit(self):
        print("Exiting the terminal. Goodbye!")
        self.continue_running = False

    @register_command("help", "Displays a list of available commands.")
    def help(self):
        print("Available commands:")
        self.command_registry.list_commands()

    def run(self):
        self.clear_screen()
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
