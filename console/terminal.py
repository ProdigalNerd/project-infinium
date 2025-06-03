import os

from console.command_registry import CommandRegistry
from console.game_manager import GameManager
from console.ui_manager import UIManager
from rich.table import Table

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
            self.ui_manager.full_clear()
            self.initialize_commands()
            self.help()

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

    def exit(self):
        print("Exiting the terminal. Goodbye!")
        self.continue_running = False

    def help(self):
        commands = self.command_registry.get_commands()
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column("Command", style="dim")
        table.add_column("Description", justify="left")
        for command in commands:
            if command.name not in self.protected_commands:
                table.add_row(command.name, command.description)

        self.ui_manager.update_game_content(table)

    def run(self):
        self.ui_manager.render()
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
