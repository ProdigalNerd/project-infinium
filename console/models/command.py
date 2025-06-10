

class Command:
    def __init__(self, name: str, description: str, execute_fn, is_available_fn=None, has_extra_args=False):
        self.name = name
        self.description = description
        self.execute_fn = execute_fn
        self.is_available_fn = is_available_fn or (lambda: True)
        self.has_extra_args = has_extra_args

    def execute(self, *args, **kwargs):
        if self.is_available():
            if self.has_extra_args:
                self.execute_fn(*args[1:])
            else:
                self.execute_fn(**kwargs)
        else:
            print(f"Command '{self.name}' is not available.")

    def is_available(self):
        return self.is_available_fn()