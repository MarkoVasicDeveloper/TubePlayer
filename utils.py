import platform
import config

if platform.system() == "Windows":
    import pygetwindow as gw
else:
    import ewmh

def get_active_window_id():

    if platform.system() == "Windows":
        active_window = gw.getActiveWindow()
        id = active_window._hWnd if active_window else None
        if(config.terminal_id): return id
        config.terminal_id = id
    else:
        ewmh_objekat = ewmh.EWMH()
        focused_window = ewmh_objekat.getActiveWindow()

        if(config.terminal_id): return focused_window.id
        config.terminal_id = focused_window.id