from game.components.has_experience import HasExperience


class Profession(HasExperience):
    def __init__(
            self,
            name: str,
            description: str,
            max_level: int = 25,
            level_cap_callback=None
            ):
        super().__init__(max_level=max_level, level_cap_callback=level_cap_callback)
        self.name = name
        self.description = description