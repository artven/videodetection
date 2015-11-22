__author__ = 'rafal'

from gi.repository import Gtk


class AboutDialog:

    def __init__(self):
        self.glade_file = "gui/about_dialog.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("about_dialog")

    def show(self):
        self.window.show()

    def on_about_dialog_response(self, object, data=None):
        self.window.hide()

if __name__ == "__main__":
    dialog = AboutDialog()
    dialog.show()
    Gtk.main()