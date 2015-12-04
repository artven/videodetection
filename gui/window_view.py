#!/usr/bin/env python3.4
__author__ = 'rafal'
__doc__ = 'Moduł głównego okna programu.'

from gi.repository import Gtk, Gdk
from gui.about_dialog import AboutDialog
from gui.settings_dialog import SettingsDialog
from gui.window_controller import WindowController
from src.logs import Logger, Database
from os import system

class ProgramView:

    def __init__(self):

        Logger.start()

        self.glade_file = "gui/main_window.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")

        # Główne widgety okna
        self.statusbar = self.builder.get_object("statusbar")
        self.context_id = self.statusbar.get_context_id("status")
        self.main_image = self.builder.get_object("main_image")
        self.toolbar = self.builder.get_object("toolbar")

        # Zmiana koloru okna
        c = Gdk.RGBA(44, 24, 44, 0.1)
        cc = Gdk.Color(255, 255, 255)
        self.window.override_background_color(Gtk.StateFlags.NORMAL, c)
        self.toolbar.override_background_color(Gtk.StateFlags.NORMAL, c)
        self.toolbar.modify_fg(Gtk.StateFlags.NORMAL, cc)

        # Elementy menu
        self.open_file_button = self.builder.get_object("open_file_button")
        self.open_camera_button = self.builder.get_object("open_camera_button")
        self.open_database_button = self.builder.get_object("open_database_button")
        self.run_alg_toggle_button = self.builder.get_object("run_alg")
        self.play_toggle_button = self.builder.get_object("play")
        self.pause_toggle_button = self.builder.get_object("pause")
        self.stop_button = self.builder.get_object("stop")
        self.record_toggle_button = self.builder.get_object("record")

        # Elementy potomne
        self.about_dialog = AboutDialog()
        self.settings_dialog = SettingsDialog()
        self.file_chooser_dialog = None

        self.main_image.set_from_file(".test.jpg")

        self.window.show()

        # Obiekt łączący algorytm z oknem
        self.controller = WindowController(self)

    def write_on_statusbar(self, text):
        self.statusbar.push(self.context_id, text)

    def enable_buttons(self):
        Logger.debug("Uaktywniono przyciski w menu.")
        self.play_toggle_button.set_active(False)
        self.pause_toggle_button.set_active(True)
        self.play_toggle_button.set_sensitive(True)
        self.pause_toggle_button.set_sensitive(True)
        self.stop_button.set_sensitive(True)
        self.record_toggle_button.set_sensitive(True)
        self.run_alg_toggle_button.set_sensitive(True)
        self.open_file_button.set_sensitive(False)

    def disable_buttons(self):
        Logger.debug("Dezaktywowano przyciski w menu.")
        self.play_toggle_button.set_sensitive(False)
        self.pause_toggle_button.set_sensitive(False)
        self.stop_button.set_sensitive(False)
        self.record_toggle_button.set_sensitive(False)
        self.run_alg_toggle_button.set_sensitive(False)
        self.open_file_button.set_sensitive(True)

    def on_open_file_button_clicked(self, object, data=None):
        self.__create_file_chooser_dialog()
        response = self.file_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            path = self.file_chooser_dialog.get_filenames()
            self.controller.set_new_files(path)
            for p in path:
                Logger.debug("Otwarto nowy plik: " + p)
            self.enable_buttons()
        self.file_chooser_dialog.destroy()
        self.file_chooser_dialog = None

    def on_open_database_clicked(self, object, data=None):
        self.__create_file_chooser_dialog(name="Open *.db file...")
        self.file_chooser_dialog.run()
        response = self.file_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            path = self.file_chooser_dialog.get_filename()
            print(path)
        self.file_chooser_dialog.destroy()
        self.file_chooser_dialog = None

        message = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.INFO)
        columns = Database.column_names_from_file(path)

        msg_text = ""
        for col in columns:
            s = "%30s" % str(col[1])
            msg_text += s + " "

        msg_text += "\n"

        i = 0
        for record in Database.read_all_records_from_file(path):
            id = record[0]
            width = record[1]
            height = record[2]
            area = record[3]
            speed = record[4]
            date = record[5].split(sep=".")[0]
            msg_text += "%30d " % id
            msg_text += "%32.2f " % width
            msg_text += "%32.2f " % height
            msg_text += "%32.2f " % area
            msg_text += "%32.2f " % speed
            msg_text += "%30s " % date
            msg_text += "\n"
            i += 1

        message.set_markup(msg_text)
        message.set_size_request(900, i*25)
        message.set_title(path)
        message.run()


    def on_open_images_clicked(self, object, data=None):
        self.controller.open_images()

    def on_delete_files_clicked(self, object, data=None):
        self.controller.delete_old_items()

    def on_play_toggled(self, object, data=None):
        is_pressed = self.play_toggle_button.get_active()
        self.pause_toggle_button.set_active(not is_pressed)
        if is_pressed:
            self.write_on_statusbar("Odtwarzanie")
            self.controller.play_file()
            self.main_image.show()

    def on_pause_toggled(self, object, data=None):
        is_pressed = self.pause_toggle_button.get_active()
        self.play_toggle_button.set_active(not is_pressed)
        if is_pressed:
            self.write_on_statusbar("Pauza")
        self.controller.pause_playing()

    def on_record_toggled(self, object, data=None):
        is_pressed = self.record_toggle_button.get_active()
        self.controller.set_recording(is_pressed)
        self.write_on_statusbar("Nagrywaj albo nie nagrywaj")

    def on_stop_clicked(self, object, data=None):
        self.pause_toggle_button.set_active(True)
        self.play_toggle_button.set_active(False)
        self.disable_buttons()
        self.controller.stop_playing()
        self.main_image.clear()
        self.write_on_statusbar("Stop")

    def on_run_alg_toggled(self, object, data=None):
        is_pressed = self.run_alg_toggle_button.get_active()
        self.controller.set_algorithm(is_pressed)
        self.write_on_statusbar("Uruchom algorytm albo nie uruchom")

    def on_about_button_clicked(self, object, data=None):
        self.write_on_statusbar("O programie")
        self.about_dialog.show()

    def on_documentation_button_clicked(self, object, data=None):
        self.write_on_statusbar("Dokumentacja")

    def on_settings_button_clicked(self, object, data=None):
        self.statusbar.push(self.context_id, "Ustawienia")
        self.settings_dialog.show()

    def on_exit_button_clicked(self, object, data=None):
        self.controller.exit()
        Gtk.main_quit()

    def on_main_window_destroy(self, object, data=None):
        self.controller.exit()
        Gtk.main_quit()

    def __create_file_chooser_dialog(self, name="Open..."):
        if self.file_chooser_dialog is None:
            self.file_chooser_dialog = Gtk.FileChooserDialog(name, None, Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            self.file_chooser_dialog.set_select_multiple(True)

if __name__ == "__main__":
    window = ProgramView()
    Gtk.main()




