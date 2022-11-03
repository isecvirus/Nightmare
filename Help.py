from rich.console import Console

nightmare_help = {
    "session": {
        "new": "Create new session.",
        "interact": "Start interacting and controlling session connection",
        "list": "List all created sessions.",
        "rename": "Change session id (it's name).",
        "remove": "Delete created session.",
    },
    "history": {
        "show": "Show commands history",
        "clear": "Clean the commands history"
    },
    "help": "Show this message and continue.",
    "clear": "Clear the screen.",
    "exit": "Exit Nightmare.",
}

session_help = {
    "set": "Set session settings and values.",
    "download": "Download a file from the victim device directly to this machine.",
    "upload": "Upload a file to the victim device directly from this machine.",

    "help": "Show this message and continue.",
    "clear": "Clear the screen.",
    "exit": "Exit the current session without disconnecting.",
    "disconnect": "Disconnect from the target server.",
}

def print_dict(d):
    console = Console()
    console.print(d, highlight=True, soft_wrap=True, no_wrap=False, markup=True, justify="full", overflow="ellipsis")

def Nightmare_help():
    print_dict(nightmare_help)
def Session_help():
    print_dict(session_help)
