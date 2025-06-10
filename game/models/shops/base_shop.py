from game.models.items.base_item import BaseItem
from rich.text import Text


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

    def get_item_to_purchase(self, ui_manager):
        output = Text()
        output.append(f"Welcome to {self.name}!\n")
        output.append(self.description + "\n\n")

        if not self.items:
            output.append("There are no items available in this shop.")
            ui_manager.update_game_content(output)
            return

        output.append("Available items:\n")
        for index, item in enumerate(self.items, start=1):
            output.append(f"{index}. {item.name} - {item.cost} gold\n")

        ui_manager.update_game_content(output)

        try:
            choice = int(input("Enter the number of the item you want to purchase: "))
            if 1 <= choice <= len(self.items):
                item = self.items[choice - 1]
                return item
            else:
                output.append("Invalid choice. Please select a valid item number.")
        except ValueError:
            output.append("Invalid input. Please enter a number.")
        
        return None
