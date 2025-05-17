from console.models.command import Command


class CommandRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.commands = {}
            self.initialized = True

    def register(self, name: str, description: str, execute_fn, is_available_fn=None, has_extra_args=False):
        self.commands[name] = Command(name, description, execute_fn, is_available_fn, has_extra_args)

    def get_command(self, name: str):
        return self.commands.get(name)
    
    def remove_command(self, name: str):
        if name in self.commands:
            del self.commands[name]

    def list_commands(self):
        for command in sorted(self.commands.values(), key=lambda cmd: cmd.name):
            if command.is_available_fn is None or command.is_available_fn():
                print(f"{command.name}: {command.description}")