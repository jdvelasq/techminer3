"""Create project structure and configuration files."""

import os

from .command_interface import CommandInterface


class ProjectStructureCreator:
    """Create the project structure."""

    def __init__(self, base_path):
        self.base_path = base_path
        self.folder_structure = {
            "databases": {},
            "my_keywords": {},
            "raw_data": {
                "cited_by": {},
                "main": {},
                "references": {},
            },
            "results": {
                "metrics": {
                    "general": {},
                    "trend": {},
                },
            },
        }

    def create_structure(self, current_structure=None, current_path=None):
        """Create the project structure."""
        if current_structure is None:
            current_structure = self.folder_structure
            current_path = self.base_path

        for name, content in current_structure.items():
            if isinstance(content, dict):  # It's a folder
                new_path = os.path.join(current_path, name)
                os.makedirs(new_path, exist_ok=True)
                self.create_structure(content, new_path)

    def execute(self):
        """Execute the command."""
        self.create_structure()


class CommandConfigCreator:
    """Creates the config files for the commands from template files."""

    def __init__(self, base_path):
        self.base_path = base_path
        self.config_files = {
            "general_metrics.py": "results/metrics/general/config.py",
            "trend_metrics.py": "results/metrics/trend/config.py",
        }

    def execute(self):
        """Create the config files."""
        for template, config in self.config_files.items():
            template_path = os.path.join(
                os.path.dirname(__file__), "..", "templates", template
            )
            config_path = os.path.join(self.base_path, config)
            # os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(template_path, "r") as template_file:
                with open(config_path, "w") as config_file:
                    config_file.write(template_file.read())


class InitCommand(CommandInterface):
    """usage: tm3 init

    Creates folder structure with configuration files.
    """

    @staticmethod
    def add_subparser(subparsers):
        """The command has not subcommands"""
        subparsers.add_parser("init", help="Initialize project structure")
        # parser.set_defaults(func=InitCommand.execute)

    def execute(self):
        """Create project structure and configuration files."""

        ProjectStructureCreator(os.getcwd()).execute()
        print("Project structure created successfully.")

        CommandConfigCreator(os.getcwd()).execute()
        print("Config files created successfully.")
        print("")
