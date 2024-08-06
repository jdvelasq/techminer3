class CommandInterface:
    def __init__(self, args):
        self.args = args

    @staticmethod
    def add_subparser(subparsers):
        raise NotImplementedError("Subclasses must implement add_subparser.")

    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")
