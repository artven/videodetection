__author__ = 'rafal'

from gi.repository import Gtk


class OkCancleDialog(Gtk.Dialog):
      def __init__(self, label_text):
        Gtk.Dialog.__init__(self, "My Dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label(label_text)
        label.set_margin_top(15)
        label.set_margin_bottom(5)
        label.set_margin_left(5)
        label.set_margin_right(5)

        self.set_title("Uwaga!")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
        self.set_modal(True)

