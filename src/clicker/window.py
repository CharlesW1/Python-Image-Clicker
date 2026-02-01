import logging
import os

try:
    import win32gui
    import win32con
except Exception:
    win32gui = None
    win32con = None

logger = logging.getLogger(__name__)


def minimize_cmd_window():
    if os.name != 'nt' or win32gui is None:
        return
    try:
        hwnd = win32gui.FindWindow("ConsoleWindowClass", None)
        if hwnd != 0:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    except Exception as e:
        logger.error("Error minimizing command prompt window: %s", e)
