__author__ = 'rafal'

from gi.repository import Gtk
from src.logs import Database


class DatabaseDialog:

    def __init__(self):
        self.glade_file = "gui/database_dialog.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)

        self.database_dialog = self.builder.get_object("database_dialog")
        self.database_dialog.hide()
        self.database_dialog.set_modal(True)
        self.database_dialog.set_destroy_with_parent(True)
        self.builder.connect_signals(self)
        self.title_label = self.builder.get_object("title_label")

        self.database_treeview = self.builder.get_object("database_treeview")
        self.database_liststore = Gtk.ListStore(int, str, str, str, str, str, str)
        self.database_treeview.set_model(self.database_liststore)
        for i, col_title in enumerate(["Nr", "Długość", "Wysokość", "Pole", "Prędkość", "Plik", "Data"]):
            render = Gtk.CellRendererText()
            coulmn = Gtk.TreeViewColumn(col_title, render, text=i)
            self.database_treeview.append_column(coulmn)

    def read_database(self, path):
        self.title_label.set_label(path)
        for record in Database.read_all_records_from_file(path):
            id = record[0]
            width = "%2.2f m" % record[1]
            height = "%2.2f m" % record[2]
            area = "%2.2f m2" % record[3]
            speed = "%2.2f km/h" % record[4]
            file = "%s" % record[5]
            date = "%s" % (record[6].split(sep=".")[0])
            self.database_liststore.append((id, width, height, area, speed, file, date))

    def on_ok_button_clicked(self, object, data=None):
        self.database_dialog.hide()

    def run(self):
        self.database_dialog.show()