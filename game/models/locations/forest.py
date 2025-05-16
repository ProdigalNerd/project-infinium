from game.models.locations.base_location import BaseLocation
from game.models.characters.goblin import Goblin
import random

class Forest(BaseLocation):
    def __init__(self, location_data):
        super().__init__(location_data)
        self.enemies = []
        
        self.load_enemies()

    def load_enemies(self):
        MIN_ENEMIES = 1
        MAX_ENEMIES = 5

        num_enemies = random.randint(MIN_ENEMIES, MAX_ENEMIES)
        self.enemies = [Goblin() for _ in range(num_enemies)]
        pass

    def describe(self):
        print(self)

    def search(self):
        self.describe()
        if self.enemies:
            print("You encounter some enemies!")
            for enemy in self.enemies:
                print(f"- {type(enemy).__name__}")
        else:
            print("The forest is quiet. You find nothing of interest.")

    def get_first_enemy(self):
        if self.enemies:
            return self.enemies.pop(0)
        return None