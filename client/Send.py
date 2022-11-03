import json


def Send(client, data: str):
    # data= [DATA] <class 'str'>
    json_data = json.dumps(data)  # "[DATA]" <class 'str'>
    client.send(json_data.encode(errors="ignore"))  # send: b"[DATA]" as <class 'bytes'>