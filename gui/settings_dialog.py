__author__ = 'rafal'

from gi.repository import Gtk
from src.config import Configuration

class SettingsDialog:


    def __init__(self):
        self.glade_file = "gui/settings_dialog.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)

        self.independent = False

        self.window = self.builder.get_object("settings_window")

        # Opcje do wprowadzanaia danych
        self.pixel_length = self.builder.get_object("pixel_length_spin_adjustment")
        self.meters_length_spin_adjustment = self.builder.get_object("meters_length_spin_adjustment")
        self.color_number_spin_adjustment = self.builder.get_object("color_number_spin_adjustment")
        self.horizontal_border_spin_adjustment = self.builder.get_object("horizontal_border_spin_adjustment")
        self.vertical_border_spin_adjustment = self.builder.get_object("vertical_border_spin_adjustment")
        self.pixel_limit_spin_adjustment = self.builder.get_object("pixel_limit_spin_adjustment")
        self.distance_from_border_spin_adjustment = self.builder.get_object("distance_from_border_spin_adjustment")

        # Pole wyboru kierunku
        self.direction_combobox = self.builder.get_object("direction_combo")
        self.direction_liststore = Gtk.ListStore(int, str)
        self.direction_liststore.append([0, "lewa->prawa"])
        self.direction_liststore.append([1, "prawa->lewa"])
        self.direction_combobox.set_model(self.direction_liststore)
        self.cell = Gtk.CellRendererText()
        self.direction_combobox.pack_start(self.cell, True)
        self.direction_combobox.add_attribute(self.cell, 'text', 1)
        # self.direction_combobox.set_active(0)
        self.direction_combobox.set_sensitive(False)

        # Opcje on-off
        self.draw_detection_region_check = self.builder.get_object("draw_detection_region_check")
        self.draw_speed_region_check = self.builder.get_object("draw_speed_region_check")
        self.draw_cars_check = self.builder.get_object("draw_cars_check")
        self.draw_conturs_check = self.builder.get_object("draw_conturs_check")
        self.draw_speed_info_check = self.builder.get_object("draw_speed_info_check")
        self.draw_size_info_check = self.builder.get_object("draw_size_info_check")
        self.draw_color_bar_check = self.builder.get_object("draw_color_bar_check")

        # Pozostałe opcje
        self.display_delay_scale_adjustment = self.builder.get_object("display_delay_scale_adjustment")

        # Przyciski
        self.cancel_button = self.builder.get_object("cancel_button")
        self.ok_button = self.builder.get_object("ok_button")
        
    def show(self):
        self.__load_settings()
        self.window.show()

    def hide(self):
        self.__write_settings()
        self.window.hide()  

    # Sygnały
    def on_settings_window_destroy(self, object, data=None):
        if self.independent:
            Gtk.main_quit()

    def on_ok_button_clicked(self, object, data=None):
        self.__write_settings()
        if self.independent:
            Gtk.main_quit()
        else:
            self.window.hide()

    def on_cancel_button_clicked(self, object, data=None):
        if self.independent:
            Gtk.main_quit()
        else:
            self.window.hide()

    def on_save_button_clicked(self, object, data=None):
        self.__write_settings()
    
    def on_restore_button_clicked(self, object, data=None):
        self.__restore_default()
        
    def on_quit_button_clicked(self, object, data=None):
        if self.independent:
            Gtk.main_quit()
        else:
            self.window.hide()

    def on_display_delay_scale_value_changed(self, object, data=None):
        print(self.display_delay_scale_adjustment.get_value())
        Configuration.play_delay(self.display_delay_scale_adjustment.get_value())

    def __load_settings(self):
        """
        Wczytaj obecną konfigurację znajdującą się config.json do widgetów okna.
        """

        Configuration.load_config()
        direct = Configuration.direction()
        if direct == "left2right":
            self.direction_combobox.set_active(0)
        else:
            self.direction_combobox.set_active(1)

        self.pixel_length.set_value(Configuration.pixel_length())
        self.meters_length_spin_adjustment.set_value(Configuration.meters_length())
        self.color_number_spin_adjustment.set_value(Configuration.color_number())
        self.horizontal_border_spin_adjustment.set_value(Configuration.horizontal_border())
        self.vertical_border_spin_adjustment.set_value(Configuration.vertical_border())
        self.pixel_limit_spin_adjustment.set_value(Configuration.pixel_limit())
        self.distance_from_border_spin_adjustment.set_value(Configuration.distance_from_border())

        self.draw_detection_region_check.set_active(Configuration.draw_detection_region())
        self.draw_speed_region_check.set_active(Configuration.draw_speed_region())
        self.draw_cars_check.set_active(Configuration.draw_cars())
        self.draw_conturs_check.set_active(Configuration.draw_conturs())
        self.draw_speed_info_check.set_active(Configuration.draw_speed_info())
        self.draw_size_info_check.set_active(Configuration.draw_size_info())
        self.draw_color_bar_check.set_active(Configuration.draw_color_bar())

    def __write_settings(self):
        """
        Zapisz wartości z widgetów
        """

        if 0 == self.direction_combobox.get_active_id():
            Configuration.direction("left2right")
        else:
            Configuration.direction("right2left")

        Configuration.pixel_length(self.pixel_length.get_value())
        Configuration.meters_length(self.meters_length_spin_adjustment.get_value())
        Configuration.color_number(self.color_number_spin_adjustment.get_value())
        Configuration.horizontal_border(self.horizontal_border_spin_adjustment.get_value())
        Configuration.vertical_border(self.vertical_border_spin_adjustment.get_value())
        Configuration.pixel_limit(self.pixel_limit_spin_adjustment.get_value())
        Configuration.distance_from_border(self.distance_from_border_spin_adjustment.get_value())

        Configuration.draw_detection_region(self.draw_detection_region_check.get_active())
        Configuration.draw_speed_region(self.draw_speed_region_check.get_active())
        Configuration.draw_cars(self.draw_cars_check.get_active())
        Configuration.draw_conturs(self.draw_conturs_check.get_active())
        Configuration.draw_speed_info(self.draw_speed_info_check.get_active())
        Configuration.draw_size_info(self.draw_size_info_check.get_active())
        Configuration.draw_color_bar(self.draw_color_bar_check.get_active())

        Configuration.save_config()

    def __restore_default(self):
        Configuration.restore_default()
        self.__load_settings()


if __name__ == "__main__":
    sd = SettingsDialog()
    sd.show()
    Gtk.main()