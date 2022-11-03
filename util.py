import os

from tabulate import tabulate
from colors import (green, reset, cyan)

def History(data:list):
    headers = [
        '%s#%s' % (green, reset),
        '%scommand%s' % (cyan, reset)
    ]
    data = zip([i for i in range(1, len(data))], data)
    return tabulate(tabular_data=data, tablefmt='plaintext', numalign='center', stralign='center', headers=headers)

def Table(headers:list or str, data:list or dict):
    return tabulate(tabular_data=data, tablefmt='plaintext', numalign='center', stralign='center', headers=headers)

def list2dict(data:list, value=None):
    return dict(zip(data, [value]*len(data)))

def file_size(file):
    if os.path.isfile(file):
        bytes = os.path.getsize(file)
        for x in ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
            if bytes < 1024:
                return "%3.3f %s" % (bytes, x)
            bytes /= 1024
def count_bytes(bytes:int):
    for x in ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if bytes < 1024:
            return "%3.3f %s" % (bytes, x)
        bytes /= 1024