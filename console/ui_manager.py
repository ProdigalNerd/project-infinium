from rich.console import Console
from rich.table import Table
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

            # Define the layout structure
            self.layout.split_column(
                Layout(name="player", size=3),
                Layout(name="game"),
            )

            self.layout["game"].split_row(
                Layout(name="player_stats", ratio=1),
                Layout(name="game_content", ratio=2),
            )

    def render(self):
        """Render the entire UI."""
        self.console.clear()
        self.console.print(self.layout)

    def update_player_stats(self, content):
        self.layout["player_stats"].update(Panel(content, title="Player Stats"))

    def update_game_content(self, content):
        self.layout["game_content"].update(Panel(content, title="Game Content"))

    def update_player(self, content):
        self.layout["player"].update(Panel(content, title="Player Info"))

    ## DELETE everything below this line ##

    def render_location(self, location):
        if location:
            panel = Panel(f"[bold cyan]{location.name}[/bold cyan]\n{location.description}", title="Current Location")
            self.console.print(panel)

    def render_inventory(self, inventory):
        table = Table(title="Inventory", show_header=True, header_style="bold green")
        table.add_column("Item", style="dim")
        table.add_column("Quantity", justify="right")

        for item, quantity in inventory.items():
            table.add_row(item.name, str(quantity))

        self.console.print(table)

    def render_message(self, message, style="bold yellow"):
        self.console.print(message, style=style)