from __future__ import annotations  # Required for forward references in type hints
import time

class CombatManager:
    def __init__(self):
        pass

    def initialize_combat(self, player: "Player", profession: "Profession", enemy: "BaseEnemy"):
        while enemy.is_alive() and player.is_alive():
            player_damage = player.calculate_attack()
            enemy.take_damage(player_damage)
            print(f"You dealt {player_damage} damage to the {type(enemy).__name__}.")
            print(f"{type(enemy).__name__} health: {enemy.current_health}/{enemy.max_health}")
            
            if not enemy.is_alive():
                print(f"You defeated the {type(enemy).__name__}!")
                profession.add_experience(enemy.get_experience_reward())
                if enemy.is_lootable():
                    player.add_loot(enemy.drop_loot())
                self.combat_target = None
                break

            time.sleep(1)

            enemy.attack_player(player)
            print(f"Current health: {player.current_health}/{player.max_health}")
            
            if not player.is_alive():
                print("You have died.")
                break

            time.sleep(1)