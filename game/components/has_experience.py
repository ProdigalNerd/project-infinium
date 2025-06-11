class HasExperience:
    def __init__(
        self,
        experience: int = 0,
        level: int = 1,
        experience_to_next_level: int = 100,
        max_level: int = 100,
        level_cap_callback=None,
        ):
        self.experience = experience
        self.level = level
        self.experience_to_next_level = experience_to_next_level
        self.max_level = max_level
        self.level_cap_callback = level_cap_callback

    def add_experience(self, amount: int):
        self.experience += amount
        if self.experience >= self.experience_to_next_level and self.level < self.max_level:
            self.level_up()

    def __increase_experience_limit__(self):
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level *= 1.5

    def level_up(self):
        self.level += 1
        if not self.is_max_level():
            self.__increase_experience_limit__()

        if self.is_max_level() and self.level_cap_callback:
            self.level_cap_callback()

    def increase_max_level(self, amount: int):
        self.max_level += amount
        self.__increase_experience_limit__()

    def is_max_level(self) -> bool:
        return self.level >= self.max_level
