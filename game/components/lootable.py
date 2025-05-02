class Lootable:
    def __init__(self, loot):
        self.loot = loot

    def drop_loot(self):
        return self.loot