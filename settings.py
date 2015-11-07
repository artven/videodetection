#!/usr/bin/env python3.4

__author__ = 'rafal'
__doc__ = "Skrypt umożliwia przegląd ustawień, bez uruchamiania całej aplikacji"

from gui.settings_dialog import SettingsDialog
from gi.repository import Gtk

if __name__ == "__main__":

    dialog = SettingsDialog()
    dialog.independent = True
    dialog.show()
    Gtk.main()