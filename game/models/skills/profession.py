from game.components.has_experience import HasExperience


class Profession(HasExperience):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
