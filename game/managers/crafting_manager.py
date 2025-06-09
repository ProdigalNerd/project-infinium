from game.models.crafting.recipe import Recipe
from game.models.inventory.inventory import Inventory


class CraftingManager:
    def __init__(self, ui_manager, update_text):
        self.crafting_queue = []
        self.ui_manager = ui_manager
        self.update_text = update_text

    def craft(self, recipe: Recipe, inventory: Inventory):
        for item in recipe.inputs:
            input_item = inventory.get_by_id(item.item_id)
            if input_item is None or input_item.quantity < item.quantity:
                self.update_text.append(f"\nNot enough {item.name} to craft {recipe.name}.")
                self.ui_manager.update_game_content(self.update_text)
                return False
            
        for item in recipe.inputs:
            inventory.remove_by_id(item.item_id, item.quantity)

        inventory.add_item(recipe.output)