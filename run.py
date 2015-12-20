#!/usr/bin/env python3

__author__ = 'rafal'
__doc__ = 'Skrypt służacy do uruchamiania programu z wiersza poleceń.'

from gi.repository import Gtk
from gui.window_view import ProgramView
from src.logs import Logger
from src.config import Configuration

if __name__ == '__main__':
    Logger.start()
    Configuration.load_config()
    window = ProgramView()
    Logger.info("Uruchamiano główne okna programu.")
    Gtk.main()