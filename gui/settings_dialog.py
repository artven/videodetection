__author__ = 'rafal'

from gi.repository import Gtk
from src.config import Configuration

class SettingsDialog:


    def __init__(self):
        self.glade_file = "gui/settings_dialog.glade"
        self.builder = Gtk.Builder()
        self.independent = False

        self.window = None
        self.border1_adjustment = None
        self.border2_adjustment = None
        self.meters_length_spin_adjustment = None
        self.color_number_spin_adjustment = None
        self.horizontal_border_spin_adjustment = None
        self.vertical_border_spin_adjustment = None
        self.pixel_limit_spin_adjustment = None
        self.distance_from_border_spin_adjustment = None
        self.draw_detection_region_check = None
        self.draw_speed_region_check = None
        self.draw_cars_check = None
        self.draw_conturs_check = None
        self.draw_speed_info_check = None
        self.draw_size_info_check = None
        self.draw_color_bar_check = None
        self.display_delay_scale_adjustment = None
        self.cancel_button = None
        self.ok_button = None

    def initialize(self):
        self.builder.add_from_file(self.glade_file)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("settings_window")
        self.window.set_modal(True)
        self.window.set_destroy_with_parent(True)

        # Opcje do wprowadzanaia danych
        self.border1_adjustment = self.builder.get_object("border1_adjustment")
        self.border2_adjustment = self.builder.get_object("border2_adjustment")
        self.meters_length_spin_adjustment = self.builder.get_object("meters_length_spin_adjustment")
        self.color_number_spin_adjustment = self.builder.get_object("color_number_spin_adjustment")
        self.horizontal_border_spin_adjustment = self.builder.get_object("horizontal_border_spin_adjustment")
        self.vertical_border_spin_adjustment = self.builder.get_object("vertical_border_spin_adjustment")
        self.pixel_limit_spin_adjustment = self.builder.get_object("pixel_limit_spin_adjustment")
        self.distance_from_border_spin_adjustment = self.builder.get_object("distance_from_border_spin_adjustment")

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

        self.initialize()
        self.__load_settings()
        self.window.show()

    def hide(self):
        self.__write_settings()
        self.window.hide()  

    # Sygnały
    def on_settings_window_destroy(self, object, data=None):
        if self.independent:
            Gtk.main_quit()
        else:
            self.window.hide()

    def on_settings_window_delete_event(self, object, data=None):
        if self.independent:
            Gtk.main_quit()
        else:
            self.window.hide()

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

        self.border1_adjustment.set_value(Configuration.distance_border1())
        self.border2_adjustment.set_value(Configuration.distance_border2())
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

        Configuration.distance_border1(self.border1_adjustment.get_value())
        Configuration.distance_border2(self.border2_adjustment.get_value())
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