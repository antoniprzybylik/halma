#!/usr/bin/python3

from ui.tui import HalmaTui
from ui.tui_generic import TerminalNotSupportedError
from ui.tui_generic import WindowTooSmallError

import sys


if __name__ == "__main__":
    tui = HalmaTui()

    try:
        tui.exec()
    except TerminalNotSupportedError:
        sys.exit('Your terminal is not supported... :(')
    except WindowTooSmallError:
        sys.exit('Your terminal window is too small... :(')
