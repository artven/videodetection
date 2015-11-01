__author__ = 'rafal'

from gi.repository import Gtk


class MyWindow:

    def __init__(self):
        self.glade_file = "main_window.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("main_window")
        self.window.show()

    def on_main_window_destroy(self, object, data=None):
        Gtk.main_quit()

    def on_exit_activate(self, object, data=None):
        Gtk.main_quit()


if __name__ == "__main__":
    window = MyWindow()
    Gtk.main()
