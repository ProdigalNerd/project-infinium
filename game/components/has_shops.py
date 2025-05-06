from game.models.shops.base_shop import BaseShop


class HasShops:
    def __init__(self, shops):
        self.shops = [BaseShop(shop) for shop in shops]
        self.visiting_shop = None

    def visit_shop(self):
        if not self.shops:
            print("There are no shops in this village.")
            return

        print("Available shops:")
        for index, shop in enumerate(self.shops, start=1):
            print(f"{index}. {shop.name}")

        try:
            choice = int(input("Enter the number of the shop you want to visit: "))
            if 1 <= choice <= len(self.shops):
                self.visiting_shop = self.shops[choice - 1]
                print(f"You visit {self.visiting_shop.name}.")
                
            else:
                print("Invalid choice. Please select a valid shop number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def leave_shop(self):
        self.visiting_shop = None
    