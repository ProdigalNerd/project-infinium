from game.components.health import HealthBar


class BaseEnemy:
    def __init__(self):
        self.attack = 5

    def attack_player(self, player):
        pass

    def get_experience_reward(self) -> int:
        return 5