import json


def Receive(client, BufferSize: int = 1024):
    data = ''
    while True:
        try:
            data += client.recv(BufferSize).decode(errors="ignore")
            json_data = json.loads(data)
            return json_data
        except ValueError:
            continue
        except (ConnectionAbortedError, AttributeError, TimeoutError):
            break
