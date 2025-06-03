class HasExperience:
    def __init__(self, experience: int = 0, level: int = 1, experience_to_next_level: int = 100):
        self.experience = experience
        self.level = level
        self.experience_to_next_level = experience_to_next_level

    def add_experience(self, amount: int):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            self.experience -= self.experience_to_next_level
            self.experience_to_next_level *= 1.5
    
    def level_up(self):
        self.level += 1
