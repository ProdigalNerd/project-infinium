class HealthBar:
    def __init__(self, max_health: int):
        self.max = max_health
        self.current = max_health

    def take_damage(self, amount: int):
        self.current -= amount
        if self.current < 0:
            self.current = 0

    def heal(self, amount: int):
        self.current += amount
        if self.current > self.max:
            self.current = self.max

    def is_alive(self) -> bool:
        return self.current > 0