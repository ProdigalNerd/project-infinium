from game.components.health import HealthBar
from game.models.characters.base_enemy import BaseEnemy


class Goblin(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.health = HealthBar(30)

    def take_damage(self, damage: int):
        self.health.take_damage(damage)

    def is_alive(self):
        return self.health.is_alive()

    def attack_player(self, player):
        print(f"Goblin attacks {player.name} for {self.attack} damage!")
        player.take_damage(self.attack)