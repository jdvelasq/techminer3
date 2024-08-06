from abc import ABC, abstractmethod

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

# Step 2: Separate Command Classes


# Step 3: Command Registry with Subcommand Execution
class CommandHandler:
    def __init__(self):
        self.commands = {
            "help": HelpCommand(),
            "refine": RefineCommand(),
            "plots": PlotCommand(),
            # Add more commands here
        }

    def execute_command(self, user_input):
        command_parts = user_input.strip().split()
        command_name = command_parts[0]
        args = command_parts[1:]

        if command_name in self.commands:
            command = self.commands[command_name]
            subcommands = command.get_subcommands()
            if args and args[0] in subcommands:
                command.execute(args)
            else:
                command.execute(args)
        else:
            print(f"Unknown command: {command_name}")


# write the command completer


def get_completer():
    command_handler = CommandHandler()
    commands = command_handler.commands
    root_completer = NestedCompleter(
        {name: command.get_subcommands() for name, command in commands.items()}
    )
    return root_completer


def main():
    root_completer = get_completer()

    while True:
        try:
            user_input = prompt("Enter command: ", completer=root_completer)
            if user_input == "exit":
                break
            CommandHandler().execute_command(user_input)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
