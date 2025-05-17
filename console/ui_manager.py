from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class UIManager:
    def __init__(self):
        self.console = Console()

    def render_player_stats(self, player):
        table = Table(title="Player Stats", show_header=True, header_style="bold magenta")
        table.add_column("Attribute", style="dim")
        table.add_column("Value", justify="right")

        table.add_row("Name", player.name)
        table.add_row("Location", player.current_location.name if player.current_location else "None")
        table.add_row("Level", str(player.level))
        table.add_row("Health", f"{player.current_health}/{player.max_health}")
        table.add_row("Experience", f"{player.experience}/{player.experience_to_next_level}")
        table.add_row("Strength", str(player.strength))
        table.add_row("Intelligence", str(player.intelligence))
        table.add_row("Agility", str(player.agility))
        table.add_row("Currency", f"{player.currency} gold")

        self.console.print(table)

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