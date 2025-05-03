class Command:
    def __init__(self, name: str, description: str, execute_fn):
        self.name = name
        self.description = description
        self.execute_fn = execute_fn

    def execute(self, *args, **kwargs):
        self.execute_fn(*args, **kwargs)