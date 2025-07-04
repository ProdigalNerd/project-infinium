from game.models.characters.base_enemy import BaseEnemy
from game.models.items.base_item import BaseItem


class Goblin(BaseEnemy):
    def __init__(self):
        super().__init__(starting_health=30)

    def attack_player(self, player):
        player.take_damage(self.attack)

    def get_loot(self):
        return [BaseItem("Goblin Gold", 50), BaseItem("Goblin Dagger", 20)]
