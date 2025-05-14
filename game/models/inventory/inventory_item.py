from game.models.items.base_item import BaseItem


class InventoryItem(BaseItem):
    def __init__(self, item_id: int, item: BaseItem, quantity: int, stackable: bool = True):
        super().__init__(item.name, item.cost)
        self.item_id = item_id
        self.quantity = quantity
        self.stackable = stackable

    def __repr__(self):
        return f"InventoryItem(item_id={self.item_id}, item_name='{self.name}', quantity={self.quantity})"