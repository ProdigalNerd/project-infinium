from __future__ import annotations  # Required for forward references in type hints
from console.command_registry import CommandRegistry
from console.ui_manager import UIManager
from game.models.skills.blacksmith import Blacksmith
from game.models.skills.miner import Miner
from game.models.skills.fighter import Fighter
from game.models.skills.woodcrafting import WoodCrafting
from game.models.skills.woodcutter import Woodcutter
from rich.table import Table

class ProfessionRegistry:
    def __init__(self, player: "Player"):
        self._professions = {
            Fighter.__name__: Fighter(player),
            Woodcutter.__name__: Woodcutter(player),
            Miner.__name__: Miner(player),
            Blacksmith.__name__: Blacksmith(player),
            WoodCrafting.__name__: WoodCrafting(player),
        }
        command_registry = CommandRegistry()
        command_registry.register(
            "list_professions",
            "List all available professions",
            self.list_professions,
        )
        self.ui_manager = UIManager()

    def list_professions(self):
        table = Table(title="Available Professions")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
        table.add_column("Level", style="green", justify="center")
        table.add_column("Experience", style="yellow", justify="center")
        for profession in self._professions.values():
            table.add_row(
                profession.name,
                profession.description,
                str(profession.level),
                str(profession.experience),
            )
        
        self.ui_manager.update_game_content(table)
