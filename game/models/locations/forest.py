from game.models.locations.base_location import BaseLocation
from game.models.characters.goblin import Goblin
import random
from rich.text import Text

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

    def search(self):
        name = Text(self.name, style="bold green", justify="left")
        description = Text(self.description, style="dim", justify="left")
        output = Text.assemble(
            name,
            "\n",
            description,
            "\n\n",
            "You search the forest...",
        )
        summary = f'You searched {self.name}'
        if self.enemies:
            output.append("\nYou encounter some enemies!")
            for enemy in self.enemies:
                output.append(f"\n- {type(enemy).__name__}")
            summary += f' and encountered {len(self.enemies)} enemies'
        else:
            output.append("\nYou find nothing of interest.")
            summary += ' but found nothing of interest'
        return output, summary

    def get_first_enemy(self):
        if self.enemies:
            return self.enemies.pop(0)
        return None