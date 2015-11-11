#!/usr/bin/env python3
__author__ = 'rafal'

from gi.repository import Gtk
from gui.window_view import ProgramView

if __name__ == "__main__":
    window = ProgramView()
    Gtk.main()