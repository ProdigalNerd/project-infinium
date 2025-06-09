import os
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

class UIManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UIManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.console = Console()
            self.layout = Layout()
            print("Initializing UIManager...")
            # Define the layout structure
            self.layout.split_column(
                Layout(name="player", size=3),
                Layout(name="game"),
            )

            self.layout["game"].split_row(
                Layout(name="player_stats", ratio=1),
                Layout(name="game_content", ratio=2),
            )
            self.initialized = True

    def full_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self):
        self.full_clear()
        self.console.print(self.layout)

    def update_player_stats(self, content):
        self.layout["player_stats"].update(Panel(content, title="Player Stats"))
        self.render()

    def update_game_content(self, content):
        self.layout["game_content"].update(Panel(content, title="Game Content"))
        self.render()

    def update_player(self, content):
        self.layout["player"].update(Panel(content, title="Player Info"))
        self.render()