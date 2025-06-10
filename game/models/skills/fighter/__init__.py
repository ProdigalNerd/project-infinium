from __future__ import annotations  # Required for forward references in type hints
from console.command_registry import CommandRegistry
from console.ui_manager import UIManager
from game.managers.combat_manager import CombatManager
from game.models.skills.profession import Profession


class Fighter(Profession):
    def __init__(self, player: "Player"):
        super().__init__(name="Fighter", description="A master of combat and physical prowess.")
        self.player_ref = player
        self.ui_manager = UIManager()

        command_registry = CommandRegistry()
        command_registry.register("fight", "Attack an enemy", self.fight, self.can_fight)

    def can_fight(self):
        location = self.player_ref.get_current_location()
        if location and hasattr(location, 'enemies') and len(location.enemies) > 0:
            return True
        return False

    def fight(self):
        location = self.player_ref.get_current_location()
        if location and hasattr(location, "get_first_enemy"):
            enemy = location.get_first_enemy()
            combat_manager = CombatManager()
            combat_manager.initialize_combat(self.player_ref, self, enemy, self.ui_manager)
        self.player_ref.display_stats()
