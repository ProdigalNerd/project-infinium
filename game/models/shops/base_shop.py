class BaseShop:
    def __init__(self, shop_data):
        self.name = shop_data.get('name', 'Unnamed Shop')
        self.description = shop_data.get('description', 'No description available.')
        self.items = shop_data.get('items', [])

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def list_items(self):
        return [item.name for item in self.items]