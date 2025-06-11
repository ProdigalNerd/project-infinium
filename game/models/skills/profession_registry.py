from __future__ import annotations  # Required for forward references in type hints
from console.command_registry import CommandRegistry
from console.ui_manager import UIManager
from game.models.skills.blacksmith import Blacksmith
from game.models.skills.miner import Miner
from game.models.skills.fighter import Fighter
from game.models.skills.woodcrafting import WoodCrafting
from game.models.skills.woodcutter import Woodcutter
from rich.table import Table
from rich.text import Text


class ProfessionRegistry:
    def __init__(self, player: "Player"):
        self._professions = {
            Fighter.__name__: Fighter(player, level_cap_callback=self.award_limit_break_points),
            Woodcutter.__name__: Woodcutter(player, level_cap_callback=self.award_limit_break_points),
            Miner.__name__: Miner(player, level_cap_callback=self.award_limit_break_points),
            Blacksmith.__name__: Blacksmith(player, level_cap_callback=self.award_limit_break_points),
            WoodCrafting.__name__: WoodCrafting(player, level_cap_callback=self.award_limit_break_points),
        }
        command_registry = CommandRegistry()
        command_registry.register(
            "list_professions",
            "List all available professions",
            self.list_professions,
        )
        self.ui_manager = UIManager()
        self.limit_break_points = 0

    def award_limit_break_points(self):
        self.limit_break_points += 1
        self.ui_manager.update_game_content(
            Text(f"You have been awarded a limit break point! Total: {self.limit_break_points}")
        )

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

    def limit_break_profession(self, profession_name: str):
        if profession_name in self._professions and self.limit_break_points > 0:
            profession = self._professions[profession_name]
            if profession.is_max_level():
                profession.increase_max_level(25)
                self.limit_break_points += 1
                self.ui_manager.update_game_content(
                    Text(f"{profession.name} has been limit broken! New max level is {profession.max_level}.")
                )
            else:
                self.ui_manager.update_game_content(
                    Text(f"{profession.name} is not at max level yet.")
                )
        else:
            self.ui_manager.update_game_content(
                Text(f"Profession {profession_name} not found.")
            )
