from typing import Callable
from console.command_registry import CommandRegistry
from console.models.command import Command

command_registry = CommandRegistry()

def register_command(name: str, description: str) -> Callable:
    def decorator(fn) -> Callable:
        # Register the command in the registry
        command_registry.register(Command(name, description, fn))
        return fn
    return decorator