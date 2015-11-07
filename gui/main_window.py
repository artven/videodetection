#!/usr/bin/env python3.4
__author__ = 'rafal'

from gi.repository import Gtk
from gui.about_dialog import AboutDialog


class ProgramController:
    pass

class ProgramView:

    def __init__(self):
        self.glade_file = "main_window.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")

        # Główne widgety okna
        self.statusbar = self.builder.get_object("statusbar")
        self.context_id = self.statusbar.get_context_id("status")
        self.main_image = self.builder.get_object("main_image")
        self.toolbar = self.builder.get_object("toolbar")

        # Elementy menu
        self.open_file_button = self.builder.get_object("open_file_button")
        self.open_camera_button = self.builder.get_object("open_camera_button")
        self.open_database_button = self.builder.get_object("open_database_button")
        self.run_alg_toggle_button = self.builder.get_object("run_alg")
        self.play_button = self.builder.get_object("play")
        self.pause_button = self.builder.get_object("pause")
        self.stop_button = self.builder.get_object("stop")
        self.record_toggle_button = self.builder.get_object("record")

        # Elementy potomne
        self.about_dialog = AboutDialog()

        # Konfiguracja widoczności elementów
        self.main_image.hide()
        self.write_on_statusbar("Witaj podróżniku!")
        self.window.show()

    def write_on_statusbar(self, text):
        self.statusbar.push(self.context_id, text)

    def on_open_file_button_clicked(self, object, data=None):
        self.write_on_statusbar("Wybierz plik")

    def on_open_camera_button_clicked(self, object, data=None):
        self.write_on_statusbar("Wybierz kamerę")

    def on_open_database_clicked(self, object, data=None):
        self.write_on_statusbar("Wybierz bazę danych z samochodami")

    def on_play_clicked(self, object, data=None):
        self.write_on_statusbar("Odtwarzanie")

    def on_pause_clicked(self, object, data=None):
        self.write_on_statusbar("Pauza")

    def on_record_toggled(self, object, data=None):
        self.write_on_statusbar("Nagrywaj albo nie nagrywaj")

    def on_stop_clicked(self, object, data=None):
        self.write_on_statusbar("Stop")

    def on_run_alg_toggled(self, object, data=None):
        self.write_on_statusbar("Uruchom algorytm albo nie uruchom")

    def on_about_button_clicked(self, object, data=None):
        self.write_on_statusbar("O programie")
        self.about_dialog.show()

    def on_documentation_button_clicked(self, object, data=None):
        self.write_on_statusbar("Dokumentacja")

    def on_settings_button_clicked(self, object, data=None):
        self.statusbar.push(self.context_id, "Ustawienia")

    def on_exit_button_clicked(self, object, data=None):
        Gtk.main_quit()

    def on_main_window_destroy(self, object, data=None):
        Gtk.main_quit()


if __name__ == "__main__":
    window = ProgramView()
    Gtk.main()




