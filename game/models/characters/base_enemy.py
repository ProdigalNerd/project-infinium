from game.components.health import HealthBar


class BaseEnemy:
    def __init__(self):
        self.health = HealthBar(5)
        self.attack = 5

    def take_damage(self, damage: int):
        pass
    
    def is_alive(self) -> bool:
        return False

    def attack_player(self, player):
        pass

    def get_experience_reward(self) -> int:
        return 5