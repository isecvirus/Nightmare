import re
from tkinter.messagebox import (showwarning, showinfo, showerror, askokcancel, askquestion, askyesno, askretrycancel, askyesnocancel)

dialog_types = [
    "error",
    "info",
    "warning",
    "ok.cancel",
    "yes.no",
    "question",
    "retry.cancel",
    "yes.no.cancel"
]

def DialogTest(dialog_settings):
    type = dialog_settings['type']
    title = dialog_settings['title']
    message = dialog_settings['message']
    response = dialog_settings['response']

    if type == 'error':
        resp = showerror(title=title, message=message)
        if response == 'true':
            print(resp)
    elif type == 'info':
        resp = showinfo(title=title, message=message)
        if response == 'true':
            print(resp)
    elif type == 'warning':
        resp = showwarning(title=title, message=message)
        if response == 'true':
            print(resp)
    elif type == 'ok.cancel':
        resp = askokcancel(title=title, message=message)
        if response == 'true':
            print(resp)
    elif type == 'yes.no':
        resp = askyesno(title=title, message=message)
        if response == 'true':
            print(resp)
    elif type == 'question':
        resp = askquestion(title=title, message=message)
        if response == 'true':
            print(resp)
    elif type == 'retry.cancel':
        resp = askretrycancel(title=title, message=message)
        if response == 'true':
            print(resp)
    elif type == 'yes.no.cancel':
        resp = askyesnocancel(title=title, message=message)
        if response == 'true':
            print(resp)