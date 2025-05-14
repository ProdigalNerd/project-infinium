from game.components.health import HealthBar
from game.components.lootable import Lootable
from game.models.characters.base_enemy import BaseEnemy
from game.models.items.base_item import BaseItem


class Goblin(BaseEnemy, HealthBar, Lootable):
    def __init__(self):
        super().__init__()
        HealthBar.__init__(self, 30)
        Lootable.__init__(self, [BaseItem("Goblin Gold", 50), BaseItem("Goblin Dagger", 20)])

    def attack_player(self, player):
        print(f"Goblin attacks {player.name} for {self.attack} damage!")
        player.take_damage(self.attack)
