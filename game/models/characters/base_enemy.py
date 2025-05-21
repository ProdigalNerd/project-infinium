from game.components.health import HealthBar


class BaseEnemy(HealthBar):
    def __init__(self, starting_health: int = 30):
        HealthBar.__init__(self, starting_health)
        self.attack = 5

    def attack_player(self, player):
        pass

    def get_experience_reward(self) -> int:
        return 5
    
    def is_lootable(self) -> bool:
        return True
    
    def get_loot(self):
        return []
    
    def drop_loot(self):
        return self.get_loot()