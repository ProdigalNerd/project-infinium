class HealthBar:
    def __init__(self, max_health: int, current_health: int):
        self.max_health = max_health
        self.current_health = current_health

    def take_damage(self, amount: int):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def heal(self, amount: int):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def is_alive(self) -> bool:
        return self.current_health > 0