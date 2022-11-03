from rich.tree import Tree
from rich import print

"""
ignore those keys hence it's not so much helpful informations to the user
"""
ignore = [
    "connector",
    "socket"
]

def TreeSessions(sessions):
    tree = Tree(label="Nightmare sessions (%s)" % len(sessions), highlight=True, expanded=True, guide_style="#222222")
    for id in sessions:
        session_data = tree.add(label=id, highlight=True)
        for session in sessions[id]:
            name = str(session).title()
            key = session_data.add(label=name, highlight=True)
            value = sessions[id][session]
            if isinstance(value, list):
                value = str(len(value))
            else:
                value = str(value)
            key.add(label=value, highlight=True)
    print(tree)

def TreeSession(id, sessions:dict):
    tree = Tree(label="Nightmare '%s' session" % id, highlight=True, expanded=True, guide_style="#222222")

    session_data = tree.add(label=id, highlight=True)
    for session in sessions[id]:
        name = str(session).title()
        key = session_data.add(label=name, highlight=True)
        value = sessions[id][session]
        if isinstance(value, list):
            value = str(len(value))
        else:
            value = str(value)
        key.add(label=value, highlight=True)
    print(tree)