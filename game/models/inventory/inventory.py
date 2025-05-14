from game.models.inventory.inventory_item import InventoryItem


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        for existing_item in self.items:
            if existing_item.name == item and existing_item.stackable:
                existing_item.quantity += 1
                print(f"Added {item} to inventory.")
                return
        
        self.items.append(InventoryItem(len(self.items) + 1, item, 1))
        print(f"Added {item} to inventory.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item} from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def list_items(self):
        if self.items:
            print("Inventory items:")
            for item in self.items:
                print(f"- {item}")
        else:
            print("Inventory is empty.")

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