from game.models.crafting.recipe_item import RecipeItem
from game.models.items.base_item import BaseItem


class Recipe:
    def __init__(self, name: str, ingredients: list[RecipeItem], result: BaseItem):
        self.name = name
        self.inputs = ingredients
        self.output = result

    def __repr__(self):
        return f"Recipe(name={self.name}, ingredients={self.inputs}, result={self.output})"
