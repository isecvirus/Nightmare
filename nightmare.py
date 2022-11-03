#!/usr/bin/env python3
import re
import sys
from prompt_toolkit import prompt, HTML, print_formatted_text
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import set_title
from Help import Nightmare_help
from Session import interact_session
from Tree import TreeSessions
from Typo import Corrections
from confirm import ConfirmPrompt
from prompt_config import prompt_style
from randomizer import Randomize
from right_prompt import RPrompt
from screen import Screen
from util import History


class Nightmare:
    """
    session values=:
    <id>: {
        <connector>: <socket-object>,
        <ip>: "192.168.100.2",
        <port>: 5600,
        <time>: "2022/10/29 02:46:23.153", (started at)
        <sent>: 5023875623, (bytes sent)
        <received>: 6239826735, (bytes received)
        <history>: ["ls", "whoami"],
        <encoding>: 'utf-8',
        <connected>: False,
        <listening>: False,
    }
    """

    def __init__(self):
        self.sessions = {}
        self.sent = 0
        self.received = 0

        self.history = []
        self.used_ports = []
        self.buffer_size = 1024
        self.default_session_ip = ""
        self.default_session_port = 800


    def run(self):
        history = InMemoryHistory()
        bindings = KeyBindings()

        @bindings.add(" ")
        def _(event):
            b = event.app.current_buffer
            w = b.document.get_word_before_cursor()

            if w is not None:
                if w in Corrections:
                    b.delete_before_cursor(count=len(w))
                    b.insert_text(Corrections[w])

            b.insert_text(" ")

        while True:
            try:
                set_title("Nightmare | 1.0.0v")

                commands = {
                    "session": {
                        "new": None,
                        "interact": {}.fromkeys(list(self.sessions.keys()), None),
                        "list": None,
                        "rename": {}.fromkeys(list(self.sessions.keys()), None),
                        "remove": {}.fromkeys(list(self.sessions.keys()), None)
                    },
                    "history": {
                        "show": None,
                        "clear": None
                    },
                    "help": None,
                    "clear": None,
                    "exit": None,
                }

                def Bottom_toolbar():
                    return [
                        ("bg:red black ", f"Session: {len(self.sessions)}"),
                    ]

                nightmare = prompt(message=HTML("<a fg='#ffffff'>Nightmare</a><a fg='#555555'>~$</a> "),
                                   refresh_interval=0.999, enable_system_prompt=True,
                                   enable_suspend=True, enable_history_search=True, search_ignore_case=True,
                                   complete_while_typing=True, completer=NestedCompleter.from_nested_dict(commands),
                                   history=history, validate_while_typing=True, wrap_lines=False,
                                   complete_in_thread=True, include_default_pygments_style=True, key_bindings=bindings,
                                   auto_suggest=AutoSuggestFromHistory(), style=prompt_style, rprompt=RPrompt,
                                   bottom_toolbar=Bottom_toolbar)
                rnightmare = re.findall("(\S+)", nightmare)  # regex nightmare input
                if len(rnightmare) > 0:
                    self.history.append(' '.join(rnightmare))

                if rnightmare:
                    if rnightmare[0] == "session":
                        if rnightmare[1] == "new":
                            random_id = Randomize().id(length=5)
                            while random_id in self.sessions:  # attempt to get unique session identifier
                                random_id = Randomize().id(length=5)
                            self.sessions[random_id] = {
                                "socket": None,
                                "connector": None,
                                "ip": self.default_session_ip,
                                "port": self.default_session_port,
                                "time": '----/--/-- --:--:--.---',
                                "sent": 0,
                                "received": 0,
                                "history": [],
                                "encoding": 'utf-8',
                                "connected": False,
                                "listening": False,
                            }
                            print_formatted_text(
                                HTML(f"<i fg='green'>New session created:</i> <b fg='#ffffff'>{random_id}</b>"))
                        elif rnightmare[1] == "interact":
                            id = rnightmare[2]
                            if id in self.sessions:
                                interact_session(sessions=self.sessions, id=id)
                        elif rnightmare[1] == "rename":
                            from_id = rnightmare[2]
                            to_id = ''.join(rnightmare[3:])
                            """
                            The above will translate a list as ["linux", "2"]..
                            .. to linux2 as a char[] aka <class 'str'>
                            """
                            if from_id in self.sessions:
                                if not to_id in self.sessions:
                                    self.sessions[to_id] = self.sessions[from_id]
                                    del self.sessions[from_id]
                                else:
                                    print("Sorry '%s' is already exist session id" % from_id)
                            else:
                                print("Sorry '%s' is not an exist session id" % from_id)
                        elif rnightmare[1] == "remove":
                            id = rnightmare[2]
                            if id in self.sessions:
                                if ConfirmPrompt(text="Session '%s' will be removed permanently, Are you sure?" % id,
                                                 title="Remove session"):
                                    self.sessions.pop(id)
                                    print_formatted_text(HTML("<i fg='green'>Removed successfully:</i> <b>%s</b>" % id))
                            else:
                                print_formatted_text(HTML("'<i fg='red'>%s</i>' <b>is not a session id.</b>" % id))
                        elif rnightmare[1] == "list":
                            TreeSessions(self.sessions)
                    elif rnightmare[0] == "history":
                        if rnightmare[1] == "show":
                            print(History(data=self.history))
                        elif rnightmare[1] == "clear":
                            self.history.clear()
                    elif rnightmare[0] == "help":
                        Nightmare_help()
                    elif rnightmare[0] == "clear":
                        Screen().clear()
                    elif rnightmare[0] == "exit":
                        allow = True
                        for id in self.sessions:
                            if self.sessions[id]['connected'] or self.sessions[id]['listening']:
                                print("You can't leave with connections behind you (CLOSE IT)")
                                allow = False
                                break
                        if allow:
                            sys.exit()
                    # else:
                    #     pass
            except (IndexError, KeyboardInterrupt):
                pass
nightmare = Nightmare()
nightmare.run()