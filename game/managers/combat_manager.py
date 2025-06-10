from __future__ import annotations  # Required for forward references in type hints
from rich.text import Text
import time

class CombatManager:
    def __init__(self):
        pass

    def initialize_combat(
            self,
            player: "Player",
            profession: "Profession",
            enemy: "BaseEnemy",
            ui_manager: "UIManager"
            ):
        output = Text()
        output.append(f"You have encountered a {type(enemy).__name__}!\n")

        while enemy.is_alive() and player.is_alive():
            player_damage = player.calculate_attack()
            enemy.take_damage(player_damage)

            output.append(f"You dealt {player_damage} damage to the {type(enemy).__name__}.\n")
            output.append(f"{type(enemy).__name__} health: {enemy.current_health}/{enemy.max_health}\n")
            
            if not enemy.is_alive():
                output.append(f"You defeated the {type(enemy).__name__}!\n")
                output.append(f"You gained {enemy.get_experience_reward()} experience.\n")
                output.append(f"You found: {enemy.drop_loot()}\n")
                profession.add_experience(enemy.get_experience_reward())
                if enemy.is_lootable():
                    player.add_loot(enemy.drop_loot())
                self.combat_target = None
                break

            ui_manager.update_game_content(output)
            time.sleep(1)

            enemy.attack_player(player)
            output.append(f"The {type(enemy).__name__} attacked you!\n")
            output.append(f"You took {enemy.attack} damage.\n")
            output.append(f"Current health: {player.current_health}/{player.max_health}\n")
            
            if not player.is_alive():
                output.append("You have been defeated!\n")
                break
            
            ui_manager.update_game_content(output)
            time.sleep(1)