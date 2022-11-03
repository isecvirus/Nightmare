import os
import random
from pyautogui import screenshot
from tempfile import NamedTemporaryFile

def ScreenShot():

    with NamedTemporaryFile(delete=False, dir='.', prefix=str(random.randint(1000000000, 9999999999)), suffix=".png") as temp:
        name = temp.name
    temp.close()

    screenshot(name)
    with open(name, "rb") as temp_ss:
        print(temp_ss.read())
    temp_ss.close()
    os.remove(name)
ScreenShot()