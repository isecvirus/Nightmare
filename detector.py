import platform


class Detector:

    def isWindows(self) -> bool:
        return ("windows" in self.operating_system())

    def isLinux(self) -> bool:
        return ("linux" in self.operating_system())

    def isDarwin(self) -> bool:
        return ("darwin" in self.operating_system())

    def isCentOs(self) -> bool:
        return ("centos" in self.operating_system())

    def isUbuntu(self) -> bool:
        return ("ubuntu" in self.operating_system())

    def isSolaris(self) -> bool:
        return ("solaris" in self.operating_system())

    def isFedora(self) -> bool:
        return ("fedora" in self.operating_system())

    def operating_system(self) -> str:
        return str(platform.system()).lower()