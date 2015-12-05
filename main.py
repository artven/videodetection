#!/usr/bin/env python3
__author__ = "Rafał Prusak"
__doc__ = "Skrypt służacy do uruchamiania programu z wiersza poleceń."

from gi.repository import Gtk
from src.logs import Logger
from src.config import Configuration
from gui.window_view import ProgramView

Logger.start()
Configuration.load_config()

Logger.info("Uruchamiano główne okna programu.")
window = ProgramView()
Gtk.main()


