from tkinter.messagebox import (showwarning, showinfo, showerror, askokcancel, askquestion, askyesno, askretrycancel, askyesnocancel)

def Dialog(client):
    settings = Receive(client=client)
    if isinstance(settings, dict):
        type = settings['type']
        title = settings['title']
        message = settings['message']

        if type == 'error':
            showerror(title=title, message=message)
        elif type == 'info':
            showinfo(title=title, message=message)
        elif type == 'warning':
            showwarning(title=title, message=message)
        elif type == 'ok.cancel':
            askokcancel(title=title, message=message)
        elif type == 'yes.no':
            askyesno(title=title, message=message)
        elif type == 'question':
            askquestion(title=title, message=message)
        elif type == 'retry.cancel':
            askretrycancel(title=title, message=message)
        elif type == 'yes.no.cancel':
            askyesnocancel(title=title, message=message)
