import datetime


def RPrompt():
    time = datetime.datetime.now().strftime("%I:%M:%S")
    period = datetime.datetime.now().strftime("%p")
    return [
        ("bg:#9800ff #ffffff", f" {time} "),
        ("bg:cornsilk fg:#9800ff", f" {period} "),
    ]