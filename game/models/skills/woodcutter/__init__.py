import random
import time
from console.command_registry import CommandRegistry
from game.enums.location_type import LocationType
from game.models.items.base_item import BaseItem
from game.models.skills.profession import Profession


class Woodcutter(Profession):
    def __init__(self, player: "Player"):
        super().__init__(name="Woodcutter", description="A master of cutting trees and gathering wood.")
        self.player_ref = player
        self.exp_per_log = 10
        self.attempts_per_action = 3
        self.time_between_actions = 1
        self.chance_of_success = 0.5

        command_registry = CommandRegistry()
        command_registry.register("chop_tree", "Chop down a tree", self.chop_tree, self.can_chop_tree)

    def can_chop_tree(self):
        location = self.player_ref.get_current_location()
        if location and location.get_type() == LocationType.FOREST:
            return True
        return False

    def chop_tree(self):
        for _ in range(self.attempts_per_action):
            if random.random() < self.chance_of_success:
                self.add_experience(self.exp_per_log)
                self.player_ref.add_loot(BaseItem("Wood", cost=1))
                print("You successfully chopped down a tree!")
            else:
                print("You failed to chop down the tree. Try again.")

            time.sleep(self.time_between_actions)
        print("You are done chopping trees for now.")