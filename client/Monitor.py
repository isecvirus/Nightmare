from screeninfo import get_monitors # python3 -m pip install screeninfo
from Tabler import Table


def Monitor():
    def DPI(width_px:int, width_mm:int):
        try:
            _ = 25.4
            px = width_px
            mm = width_mm
            return px / (mm / _)
        except ZeroDivisionError:
            return "0"

    monitors = {}

    for monitor in get_monitors():
        name = str(monitor.name)
        width_px = monitor.width
        width_mm = monitor.width_mm
        monitors[name] = {
            "name": name,
            "x": str(monitor.x),
            "y": str(monitor.y),
            "width (px)": str(width_px),
            "height (px)": str(monitor.height),
            "width (mm)": str(width_mm),
            "height (mm)": str(monitor.height_mm),
            "dpi": str(DPI(width_px=width_px, width_mm=width_mm)),
            "is_primary": str(monitor.is_primary),
        }
    return Table(headers='keys', data=monitors.values())
