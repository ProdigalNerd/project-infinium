class HasExperience:
    def __init__(self, experience: int = 0):
        self.experience = experience
        self.level = 1
        self.experience_to_next_level = 100

    def add_experience(self, amount: int):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            self.experience -= self.experience_to_next_level
            self.experience_to_next_level *= 1.5
    
    def level_up(self):
        self.level += 1
