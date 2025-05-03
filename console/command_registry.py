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

    def register(self, command: Command):
        self.commands[command.name] = command

    def get_command(self, name: str):
        if name in self.commands:
            print(f"Command found: {name}")
        else:
            print(f"Command not found: {name}")
        return self.commands.get(name)
    
    def remove_command(self, name: str):
        if name in self.commands:
            del self.commands[name]

    def list_commands(self):
        for command in sorted(self.commands.values(), key=lambda cmd: cmd.name):
            print(f"{command.name}: {command.description}")