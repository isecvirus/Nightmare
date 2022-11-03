import platform

from Monitor import Monitor


def Get_info():
    info = ""
    info += f"System                : {platform.system()}\n"
    info += f"Platform              : {platform.platform()}\n"
    info += f"Processor             : {platform.processor()}\n"
    info += f"Release               : {platform.release()}\n"
    info += f"Win32 edition         : {platform.win32_edition()}\n"
    info += f"Win32 is iot          : {platform.win32_is_iot()}\n"
    info += f"Win32 version         : {platform.win32_ver()}\n"
    info += f"Python branch         : {platform.python_branch()}\n"
    info += f"Python build          : {', '.join(platform.python_build())}\n"
    info += f"Python compiler       : {platform.python_compiler()}\n"
    info += f"Python implementation : {platform.python_implementation()}\n"
    info += f"Python revision       : {platform.python_revision()}\n"
    info += f"\n" + Monitor() + "\n"
    return info
