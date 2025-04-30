class BaseEnemy:
    def __init__(self):
        self.current_health = 30
        self.attack = 5

    def take_damage(self, damage: int):
        pass
    
    def is_dead(self) -> bool:
        return False

    def attack_player(self, player):
        pass

    def get_experience_reward(self) -> int:
        return 5