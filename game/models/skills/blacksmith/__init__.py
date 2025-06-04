from console.command_registry import CommandRegistry
from game.models.skills.profession import Profession


class Blacksmith(Profession):
    def __init__(self, player: "Player"):
        super().__init__(name="Blacksmith", description="A master of crafting and repairing weapons and armor.")
        self.player_ref = player
        self.exp_per_item = 20
        self.attempts_per_action = 2
        self.time_between_actions = 1.5
        self.chance_of_success = 0.7

        # Register commands specific to the Blacksmith profession
        command_registry = CommandRegistry()
        command_registry.register("smelt_ore", "Smelt ore into bars", self.smelt_ore, self.can_smelt_ore)
        command_registry.register("forge_item", "Forge a new item", self.forge_item, self.can_forge_item)

    def can_smelt_ore(self):
        # Logic to determine if the player can smelt ore
        return True
    
    def can_forge_item(self):
        # Logic to determine if the player can forge an item
        return True

    def smelt_ore(self):
        # Logic for smelting ore into bars
        print("Smelting ore into bars...")
        # Add experience and loot logic here

    def forge_item(self):
        # Logic for forging an item
        print("Forging a new item...")
        # Add experience and loot logic here
