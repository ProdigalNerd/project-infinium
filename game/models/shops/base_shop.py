from game.models.items.base_item import BaseItem


class BaseShop:
    def __init__(self, shop_data):
        self.name = shop_data.get('name', 'Unnamed Shop')
        self.description = shop_data.get('description', 'No description available.')
        self.items = [BaseItem(**item) for item in shop_data.get('items', [])]

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def list_items(self):
        for item in self.items:
            print(f"{item.name} - {item.cost} gold")

    def purchase_item(self, player):
        if not self.items:
            print("There are no items in this shop.")
            return

        print("Available items:")
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item.name}")

        try:
            choice = int(input("Enter the number of the item you want to purchase: "))
            if 1 <= choice <= len(self.items):
                item = self.items[choice - 1]
                if player.currency >= item.cost:
                    player.currency -= item.cost
                    player.inventory.add_item(item)
                    self.remove_item(item)
                    print(f"You purchased {item.name} for {item.cost} gold.")
            else:
                print("Invalid choice. Please select a valid shop number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
