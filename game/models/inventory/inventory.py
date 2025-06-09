from console.ui_manager import UIManager
from game.models.inventory.inventory_item import InventoryItem
from rich.table import Table
from rich.text import Text as RichText


class Inventory:
    def __init__(self):
        self.items = []
        self.ui_manager = UIManager()

    def add_item(self, item, quantity=1):
        for existing_item in self.items:
            if existing_item.name == item and existing_item.stackable:
                existing_item.quantity += quantity
                print(f"Added {item} to inventory.")
                return
        
        if isinstance(item, InventoryItem):
            self.items.append(item)
            return
        
        self.items.append(InventoryItem(len(self.items) + 1, item, quantity))

    def get_by_id(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item} from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def remove_by_id(self, item_id, quantity=1):
        item = self.get_by_id(item_id)
        if item:
            if item.quantity >= quantity:
                item.quantity -= quantity
                if item.quantity == 0:
                    self.items.remove(item)
                print(f"Removed {quantity} of {item.name} from inventory.")
            else:
                print(f"Not enough {item.name} to remove. Available: {item.quantity}, Requested: {quantity}.")
        else:
            print(f"Item with ID {item_id} not found in inventory.")

    def list_items(self):
        if self.items:
            table = Table(title="Inventory Items")
            table.add_column("Name", style="magenta")
            table.add_column("Quantity", justify="right", style="green")

            for item in self.items:
                table.add_row(item.name, str(item.quantity))

            self.ui_manager.update_game_content(table)
        else:
            self.ui_manager.update_game_content(RichText("Your inventory is empty.", style="bold red"))

    def sort_items(self):
        self.items.sort()
        print("Inventory sorted.")

    def select_item(self):
        if not self.items:
            print("There are no items in this shop.")
            return

        print("Available items:")
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item.name}")

        try:
            choice = int(input("Enter the number of the item you want to sell: "))
            if 1 <= choice <= len(self.items):
                item = self.items[choice - 1]
                return item
            else:
                print("Invalid choice. Please select a valid shop number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        return None