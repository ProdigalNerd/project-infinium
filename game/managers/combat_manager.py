import time

class CombatManager:
    def __init__(self):
        pass

    def initialize_combat(self, player, enemy):
        while enemy.is_alive() and player.is_alive():
            player_damage = player.calculate_attack()
            enemy.take_damage(player_damage)
            print(f"You dealt {player_damage} damage to the {type(enemy).__name__}.")
            
            if not enemy.is_alive():
                print(f"You defeated the {type(enemy).__name__}!")
                player.add_experience(enemy.get_experience_reward())
                self.combat_target = None
                break

            time.sleep(1)

            enemy.attack_player(player)
            print(f"Current health: {player.health.current}/{player.health.max}")
            
            if not player.is_alive():
                print("You have died.")
                break

            time.sleep(1)