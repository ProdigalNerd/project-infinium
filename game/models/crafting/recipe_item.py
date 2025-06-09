from game.models.items.base_item import BaseItem


class RecipeItem(BaseItem):
    def __init__(self, item_id: int, item: BaseItem, quantity: int):
        super().__init__(item.name, item.cost)
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        return f"RecipeItem(item_id='{self.item_id}', item_name='{self.name}', quantity={self.quantity})"