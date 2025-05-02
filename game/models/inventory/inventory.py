class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
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