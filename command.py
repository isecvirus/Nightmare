from prompt_toolkit.completion import PathCompleter

class Commands:
    def __init__(self):
        self.commands = {
            "download": None,
            "upload": None,
        }
    def valid(self, command):
        return command in self.commands