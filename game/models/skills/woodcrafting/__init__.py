from console.command_registry import CommandRegistry
from game.models.skills.profession import Profession


class WoodCrafting(Profession):
    def __init__(self, player: "Player"):
        super().__init__(name="WoodCrafting", description="A master of crafting and working with wood.")
        self.player_ref = player
        self.exp_per_item = 15
        self.attempts_per_action = 2
        self.time_between_actions = 1.0
        self.chance_of_success = 0.8

        # Register commands specific to the WoodCrafting profession
        command_registry = CommandRegistry()
        command_registry.register("craft_item", "Craft a wooden item", self.craft_item, self.can_craft_item)

    def can_craft_item(self):
        # Logic to determine if the player can craft a wooden item
        return True

    def craft_item(self):
        # Logic for crafting a wooden item
        print("Crafting a wooden item...")
        # Add experience and loot logic here