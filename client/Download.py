import os
import socket


def Download_file(client, filename, BufferSize:int=1024):
    filename = os.path.split(filename)[-1]
    file_obj = open(filename, 'wb')

    client.settimeout(1) # to manage EOF
    try:
        chunk = client.recv(BufferSize)
        if chunk:
            while chunk:
                file_obj.write(chunk)
                try:
                    chunk = client.recv(BufferSize)
                except (socket.timeout, TimeoutError) as e:
                    break # after 1 second if no response file will be closed..
        else:
            return
    except (socket.timeout, TimeoutError):
        return
    client.settimeout(None) # and timeout will be reset to None (which means infinity)
    file_obj.close()
