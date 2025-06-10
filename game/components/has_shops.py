from game.models.shops.base_shop import BaseShop
from rich.text import Text


class HasShops:
    def __init__(self, shops):
        self.shops = [BaseShop(shop) for shop in shops]
        self.visiting_shop = None

    def visit_shop(self, ui_manager):
        output = Text()
        if not self.shops:
            output.append("There are no shops in this village.", style="bold red")
            ui_manager.update_game_content(output)
            return

        output.append("You can visit the following shops:\n", style="bold green")
        for index, shop in enumerate(self.shops, start=1):
            output.append(f"{index}. {shop.name}\n", style="bold blue")
        
        ui_manager.update_game_content(output)

        try:
            choice = int(input("Enter the number of the shop you want to visit: "))
            if 1 <= choice <= len(self.shops):
                self.visiting_shop = self.shops[choice - 1]
                output.append(f"You visit {self.visiting_shop.name}.", style="bold yellow")
                ui_manager.update_game_content(output)
                
            else:
                output.append("Invalid choice. Please select a valid shop number.", style="bold red")
                ui_manager.update_game_content(output)
        except ValueError:
            output.append("Invalid input. Please enter a number.", style="bold red")
            ui_manager.update_game_content(output)

    def leave_shop(self):
        self.visiting_shop = None
    