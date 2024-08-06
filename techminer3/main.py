"""Entry point for the techminer3 command-line interface.

"""

import argparse

from techminer3.commands.init_command import InitCommand


def main():
    """Entry point for the techminer3 command-line interface."""

    parser = argparse.ArgumentParser(
        usage="tm3 COMMAND [ARGS]",
        description="A runtime for bibliometric analysis and tech-mining",
        add_help=False,  # This disables the default '-h/--help' option
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help=None,
        title="Commands",
        description=None,
    )

    # Define command instances for each command class
    command_instances = {
        "init": InitCommand,
    }

    for command_class in command_instances.values():
        command_class.add_subparser(subparsers)

    args = parser.parse_args()

    if args.command and args.command in command_instances:
        command_instance = command_instances[args.command](args)
        command_instance.execute()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
