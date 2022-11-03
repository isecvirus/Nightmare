import random
from prompt_toolkit import prompt, HTML


def Exit():
    code = random.randint(1000, 9999)
    isCode = prompt(HTML('To continue exiting enter the code (<b fg="red">%s</b>): ' % code))
    if isCode == str(code):
        exit()
    exit()