class InventoryItem:
    def __init__(self, item_id: int, name: str, quantity: int, stackable: bool = True):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.stackable = stackable

    def __repr__(self):
        return f"InventoryItem(item_id={self.item_id}, item_name='{self.name}', quantity={self.quantity})"