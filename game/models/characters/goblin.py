from game.models.characters.base_enemy import BaseEnemy


class Goblin(BaseEnemy):
    def __init__(self):
        super().__init__()

    def take_damage(self, damage: int):
        self.current_health -= damage

    def is_dead(self):
        if self.current_health <= 0:
            print("Goblin has been defeated!")
            return True
        return False

    def attack_player(self, player):
        print(f"Goblin attacks {player.name} for {self.attack} damage!")
        player.take_damage(self.attack)