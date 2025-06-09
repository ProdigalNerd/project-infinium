from console.command_registry import CommandRegistry
from console.ui_manager import UIManager
from game.managers.crafting_manager import CraftingManager
from game.models.crafting.recipe import Recipe
from game.models.crafting.recipe_item import RecipeItem
from game.models.items.base_item import BaseItem
from game.models.skills.profession import Profession
from rich.text import Text


class WoodCrafting(Profession):
    def __init__(self, player: "Player"):
        super().__init__(name="WoodCrafting", description="A master of crafting and working with wood.")
        self.player_ref = player
        self.exp_per_item = 15
        self.attempts_per_action = 2
        self.time_between_actions = 1.0
        self.chance_of_success = 0.8
        self.ui_manager = UIManager()

        self.recipes = [
            Recipe("Wood Plank", 
                   ingredients=[RecipeItem(item_id=2, item=BaseItem("Wood", 2), quantity=2)],
                   result=BaseItem("Wood Plank", 5)),
        ]

        # Register commands specific to the WoodCrafting profession
        command_registry = CommandRegistry()
        command_registry.register("craft_item", "Craft a wooden item", self.craft_item, self.can_craft_item)

    def can_craft_item(self):
        # Logic to determine if the player can craft a wooden item
        return True

    def craft_item(self):
        self.list_recipes()
        self.ui_manager.render()
        choice = int(input("Enter the number of the item you want to craft: "))
        if 0 <= choice < len(self.recipes):
            recipe = self.recipes[choice]

            update_text = Text(f"Crafting {recipe.name}...")
            self.ui_manager.update_game_content(update_text)
            self.ui_manager.render()
            
            CraftingManager().craft(recipe, self.player_ref.inventory)
            
            update_text.append(f"\n{recipe.name} crafted successfully!")
            self.ui_manager.update_game_content(update_text)
            self.ui_manager.render()
        else:
            print("Invalid choice. Please select a valid recipe number.")
        
    def list_recipes(self):
        recipe_list = Text()
        counter = 0
        for recipe in self.recipes:
            recipe_list.append(f"{counter}) {recipe.name}\n")
            counter += 1
        
        self.ui_manager.update_game_content(recipe_list)