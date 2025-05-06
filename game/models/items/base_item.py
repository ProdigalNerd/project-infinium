class BaseItem:
    def __init__(self, name: str, cost: float):
        self.name = name
        self.cost = cost

    def __str__(self):
        return f"{self.name}"