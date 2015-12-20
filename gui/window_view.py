#!/usr/bin/env python3.4
__author__ = 'rafal'
__doc__ = 'Moduł głównego okna programu.'

from gi.repository import Gtk
from gui.about_dialog import AboutDialog
from gui.settings_dialog import SettingsDialog
from gui.window_controller import WindowController


class ProgramView:

    def __init__(self):

        # Okno programu
        self.glade_file = "gui/main_window.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("main_window")

        # Obiekt łączący algorytm z oknem
        self.controller = WindowController(self)

        # Główne widgety okna
        self.statusbar = self.builder.get_object("statusbar")
        self.context_id = self.statusbar.get_context_id("status")
        self.main_image = self.builder.get_object("main_image")
        self.toolbar = self.builder.get_object("toolbar")

        # Wygenerowanie elementów menu odtwarzania
        self.play_button = self.builder.get_object("play_button")
        self.pause_button = self.builder.get_object("pause_button")
        self.stop_button = self.builder.get_object("stop_button")
        self.replay_button = self.builder.get_object("replay_button")
        self.record_toggle_button = self.builder.get_object("record_toggle_button")
        self.run_alg_toggle_button = self.builder.get_object("run_alg_button")
        self.display_mask_button = self.builder.get_object("display_mask_button")

        # Wygnerowanie elementów głównego menu
        self.open_file_button = self.builder.get_object("open_file_button")
        self.open_database_button = self.builder.get_object("open_database_button")
        self.open_images_button = self.builder.get_object("open_images_button")
        self.delete_files_button = self.builder.get_object("delete_files_button")
        self.settings_button = self.builder.get_object("settings_button")
        self.documentation_button = self.builder.get_object("documentation_button")
        self.about_button = self.builder.get_object("about_button")

        # Pasek postępu
        self.progressbar = self.builder.get_object("progressbar")

        # Elementy potomne
        self.about_dialog = AboutDialog()
        self.settings_dialog = SettingsDialog()
        self.file_chooser_dialog = None

        # ustawienie pustego obrazu startowego
        self.controller.clear_main_image()

        # Lista wykrytych samochodów
        self.detected_cars_liststore = Gtk.ListStore(int, str, str, str, str, str, str)
        self.detected_cars_treeview = self.builder.get_object("detected_cars_treeview")
        self.detected_cars_treeview.set_model(self.detected_cars_liststore)
        for i, col_title in enumerate(["Nr", "Długość", "Wysokość", "Pole", "Prędkość", "Kolor", "Plik"]):
            render = Gtk.CellRendererText()
            coulmn = Gtk.TreeViewColumn(col_title, render, text=i)
            self.detected_cars_treeview.append_column(coulmn)

        # Lista plików
        self.files_liststore = Gtk.ListStore(int, str)
        self.files_treeview = self.builder.get_object("files_treeview")
        self.files_treeview.set_model(self.files_liststore)
        for i, col_title in enumerate(["Nr", "Ścieżka"]):
            render = Gtk.CellRendererText()
            coulmn = Gtk.TreeViewColumn(col_title, render, text=i)
            self.files_treeview.append_column(coulmn)

        self.files_treeview.connect('button-press-event', self.button_press_event)

        # Uruchomienie głównego okna
        self.window.show()

    def write_on_statusbar(self, text):
        self.statusbar.push(self.context_id, text)

    # Funkcje obsługujące przyciski menu odtwarzania

    def on_play_button_clicked(self, object, data=None):
        self.controller.start_playing()
        self.write_on_statusbar("Odtwarzanie...")

    def on_pause_button_clicked(self, object, data=None):
        self.controller.pause_playing()
        self.write_on_statusbar("Pauza")

    def on_stop_clicked(self, object, data=None):
        self.controller.stop_playing()
        self.controller.clear_main_image()
        self.write_on_statusbar("Stop")

    def on_replay_clicked(self, object, data=None):
        self.controller.replay()
        self.write_on_statusbar("Ponowne odtwarzanie...")

    def on_record_toggled(self, object, data=None):
        is_pressed = self.record_toggle_button.get_active()
        self.controller.enable_recording(is_pressed)
        if is_pressed:
            self.write_on_statusbar("Nagrywanie włączone.")
        else:
            self.write_on_statusbar("Nagrywanie wyłączone.")

    def on_run_alg_toggled(self, object, data=None):
        is_pressed = self.run_alg_toggle_button.get_active()
        self.controller.enable_algorithm(is_pressed)
        if is_pressed:
            self.write_on_statusbar("Przetwarzanie obrazu włączone.")
        else:
            self.write_on_statusbar("Przetwarzanie obrazu wyłączone.")

    def on_display_mask_button_toggled(self, object, data=None):
        is_pressed = self.display_mask_button.get_active()
        self.controller.enable_mask(is_pressed)
        if is_pressed:
            self.write_on_statusbar("Wyświetlnanie maski włączone.")
        else:
            self.write_on_statusbar("Wyświetlnanie maski wyłączone.")

    # Funkcje obsługujące przyciski głównego menu

    def on_open_file_button_clicked(self, object, data=None):
        self.write_on_statusbar("Otwieranie nowych plików.")
        self.controller.open_files()

    def on_open_database_clicked(self, object, records_text=None):
        self.write_on_statusbar("Otwieranie bazy danych.")
        self.controller.open_database()

    def on_open_images_clicked(self, object, data=None):
        self.write_on_statusbar("Przeglądanie obrazów.")
        self.controller.open_images()

    def on_delete_files_clicked(self, object, data=None):
        self.write_on_statusbar("Usuwanie plików.")
        self.controller.clear_data()

    def on_settings_button_clicked(self, object, data=None):
        self.write_on_statusbar("Ustawienia.")
        self.settings_dialog.show()

    def on_documentation_button_clicked(self, object, data=None):
        self.write_on_statusbar("Dokumentacja.")
        self.controller.open_documentation()

    def on_about_button_clicked(self, object, data=None):
        self.write_on_statusbar("O programie.")
        self.about_dialog.show()

    def on_exit_button_clicked(self, object, data=None):
        self.write_on_statusbar("Wychodznie z programu.")
        self.controller.exit()
        Gtk.main_quit()

    def on_main_window_destroy(self, object, data=None):
        self.controller.exit()
        Gtk.main_quit()

    # Usuwanie plików z listy
    def button_press_event(self, treeview, event):
        print("sajonara")
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            path_info = treeview.get_path_at_pos(x, y)
            self.controller.remove_element(path_info)
