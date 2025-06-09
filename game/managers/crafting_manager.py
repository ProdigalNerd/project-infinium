from game.models.crafting.recipe import Recipe
from game.models.inventory.inventory import Inventory


class CraftingManager:
    def __init__(self):
        self.crafting_queue = []

    def craft(self, recipe: Recipe, inventory: Inventory):
        for item in recipe.inputs:
            input_item = inventory.get_by_id(item.item_id)
            if input_item is None or input_item.quantity < item.quantity:
                print(f"Not enough {item.name} to craft {recipe.name}.")
                return False
            
        for item in recipe.inputs:
            inventory.remove_by_id(item.item_id, item.quantity)

        inventory.add_item(recipe.output)