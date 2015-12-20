#!/usr/bin/env python3

__author__ = 'rafal'
__doc__ = 'Skrypt służacy do uruchamiania programu z wiersza poleceń.'

from gi.repository import Gtk
from gui.window_view import ProgramView
from src.logs import Logger
from src.config import Configuration

if __name__ == '__main__':
    Configuration.load_config()
    Logger.start()
    window = ProgramView()
    Logger.info("Uruchamiano główne okna programu.")
    Gtk.main()