class Command:
    def __init__(self, name: str, description: str, execute_fn, is_available_fn=None):
        self.name = name
        self.description = description
        self.execute_fn = execute_fn
        self.is_available_fn = is_available_fn or (lambda: True)

    def execute(self, *args, **kwargs):
        if self.is_available():
            self.execute_fn(*args, **kwargs)
        else:
            print(f"Command '{self.name}' is not available.")

    def is_available(self):
        return self.is_available_fn()