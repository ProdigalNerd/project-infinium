from game.components.health import HealthBar
from game.models.characters.base_enemy import BaseEnemy


class Goblin(BaseEnemy, HealthBar):
    def __init__(self):
        super().__init__()
        HealthBar.__init__(self, 30)

    def attack_player(self, player):
        print(f"Goblin attacks {player.name} for {self.attack} damage!")
        player.take_damage(self.attack)