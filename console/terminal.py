from ast import arg
import os

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
            self.commands = {
                "help": { "fn": self.help, "remove_after_run": False },
                "exit": { "fn": self.exit, "remove_after_run": False },
                "clear": { "fn": self.clear_screen, "remove_after_run": False },
            }
            self.game_manager = GameManager()
            self.setup_commands()

    def setup_commands(self):
        game_commands = self.game_manager.get_terminal_commands()
        for command_name, command_function, remove_after_run in game_commands:
            self.add_command(command_name, command_function, remove_after_run)

    def add_command(self, command_name, command_function, remove_after_run=False):
        if command_name not in self.commands:
            self.commands[command_name] = {
                "fn": command_function,
                "remove_after_run": remove_after_run
            }

    def removeCommand(self, command_name):
        if command_name in self.commands and command_name not in self.protected_commands:
            del self.commands[command_name]

    def clear_screen(self):
        # Clear the console screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def exit(self):
        # Exit the terminal
        print("Exiting the terminal. Goodbye!")
        self.continue_running = False

    def help(self):
        # Display help information
        print("Available commands:")
        for command in self.commands:
            print(f"- {command}")

    def run(self):
        self.clear_screen()
        print("Welcome to the terminal! Type 'help' for a list of commands.")
        while self.continue_running:
            command_input = input("> ").strip().lower()
            parts = command_input.split()
            
            if not parts:
                continue

            command = parts[0]
            args = parts[1:]

            if command in self.commands:
                self.commands[command]["fn"](*args)
                if self.commands[command]["remove_after_run"]:
                    self.removeCommand(command)
                self.setup_commands()
            else:
                print(f"Unknown command: {command}")
