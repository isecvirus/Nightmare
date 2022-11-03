import subprocess

from detector import Detector
class Screen:
    def clear(self):
        windows = Detector().isWindows()
        linux = Detector().isLinux()
        if windows:
            subprocess.call("cls", shell=True, stderr=subprocess.PIPE)
        elif linux:
            subprocess.call("clear", shell=True, stderr=subprocess.PIPE)