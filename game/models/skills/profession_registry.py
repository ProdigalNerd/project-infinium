from __future__ import annotations  # Required for forward references in type hints
from game.models.skills.fighter import Fighter


class ProfessionRegistry:
    def __init__(self, player: "Player"):
        self._professions = {
            Fighter.__name__: Fighter(player),
        }

    def list_professions(self):
        for profession in self._professions.values():
            print(f"Name: {profession.name}, Description: {profession.description}, Level: {profession.level}")