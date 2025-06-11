import random
import time
from console.command_registry import CommandRegistry
from game.enums.location_type import LocationType
from game.models.items.base_item import BaseItem
from game.models.skills.profession import Profession


class Miner(Profession):
    def __init__(self, player: "Player", level_cap_callback):
        super().__init__(
            name="Miner",
            description="A master of cutting trees and gathering wood.",
            level_cap_callback=level_cap_callback
            )
        self.player_ref = player
        self.exp_per_log = 10
        self.attempts_per_action = 3
        self.time_between_actions = 1
        self.chance_of_success = 0.5

        command_registry = CommandRegistry()
        command_registry.register("mine_ore", "Mine some ore", self.mine_ore, self.can_mine_ore)

    def can_mine_ore(self):
        location = self.player_ref.get_current_location()
        if location and location.get_type() == LocationType.PLAINS or location.get_type() == LocationType.MOUNTAIN:
            return True
        return False

    def mine_ore(self):
        for _ in range(self.attempts_per_action):
            if random.random() < self.chance_of_success:
                self.add_experience(self.exp_per_log)
                self.player_ref.add_loot(BaseItem("Ore", cost=1))
                print("You successfully mined some ore!")
            else:
                print("You failed to mine any ore. Try again.")

            time.sleep(self.time_between_actions)
        print("You are done mining for now.")