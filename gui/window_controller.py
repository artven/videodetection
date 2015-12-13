__author__ = 'rafal'

import os
import shutil
import cv2

from src.video import VideoReader, VideoWriter
from gi.repository import Gtk, GdkPixbuf, GLib
from src.logs import Database, ImageSaver, Logger
from src.alg import Algorithm
from src.video import Frame
from src.config import Configuration
from os import system

from gui.database_dialog import DatabaseDialog


class WindowController:

    tmp_images_directory = "/tmp/loaded_file"

    def __init__(self, window):

        Logger.start()
        Configuration.load_config()

        self.window = window

        # Pliki wejściowe
        self.__input_video = None
        self.__played_file = 0

        # Flagi programu
        self.__play_file_flag = False
        self.__exit_flag = False
        self.__run_alg_flag = False
        self.__display_mask_flag = False
        self.__record_video_flag = False

        self.__output_video = None
        self.__loaded_frames = 0
        self.__current_frame_index = 1
        self.__record_index = 1

        self.__file_number = 0

        self.database = None
        self.img_saver = ImageSaver()
        GLib.timeout_add(100, self.algorithm)

    # Funkcje obsługujące przyciski głownego meunu

    def open_files(self):
        name = "Wybierz pliki wideo..."
        response = self.__run_file_chooser_dialog(name)

        if response is not None:
            # Sprawdzenie poprawności ścieżek do plików
            for path in response:
                if not self.__video_path_valid(path):
                    self.window.write_on_statusbar("Wybrano błędy plik!")
                    Logger.error("Przy otwieraniu plików wykryto błędny plik.")
                else:
                    self.__add_file_to_list(path)

            if self.__files_list_length():
                self.__play_button_enable(True)

    def open_database(self):
        name = "Wybierz bazę danych"
        response = self.__run_file_chooser_dialog(name, allow_multiple=False)

        if response is not None:
            path = response[0]
            if not self.__database_path_valid(path):
                self.window.write_on_statusbar("Wybrano zły plik!")
                Logger.error("Wybrano zły plik bazy danych.")
            else:
                dialog = DatabaseDialog()
                dialog.read_database(path)
                dialog.run()

    def open_images(self):
        os.system("eog " + "images/")

    def clear_data(self):
        shutil.rmtree('images')
        shutil.rmtree('data')
        os.mkdir('images')
        os.mkdir('data')
        os.mknod("images/.keepfile")
        os.mknod("data/.keepfile")
        self.database = Database()

    def open_documentation(self):
        system("firefox doc/index.html")

    def exit(self):
        self.__exit_flag = True

    # Funkcje obsługujące przyciski menu odtwarzania

    def start_playing(self):
        if self.database is None and self.__run_alg_flag:
            self.database = Database()
        self.__preprare_directory()
        self.__play_button_enable(False)
        self.__pause_button_enable(True)
        self.__replay_button_enable(False)
        self.__stop_button_enable(True)
        self.__open_files_button_enable(False)
        self.__play_file_flag = True
        self.__enable_main_menu(False)

    def pause_playing(self):
        self.__play_file_flag = False
        self.__play_button_enable(True)
        self.__pause_button_enable(False)
        self.__replay_button_enable(True)
        self.__stop_button_enable(True)

    def stop_playing(self):
        self.__play_file_flag = False
        self.__played_file = 1
        self.__input_video = None
        self.__play_button_enable(True)
        self.__pause_button_enable(False)
        self.__replay_button_enable(False)
        self.__stop_button_enable(False)
        self.__open_files_button_enable(True)
        self.__enable_main_menu(True)

    def replay(self):
        self.__play_file_flag = False
        self.__input_video = None
        self.__played_file = 0
        self.start_playing()

    def enable_recording(self, value):
        self.__record_video_flag = value

    def enable_algorithm(self, value):
        self.__run_alg_flag = value

    def enable_mask(self, value):
        self.__display_mask_flag = value

    # Lista plików

    def __add_file_to_list(self, path):
        self.__file_number += 1
        nr = self.__file_number
        self.window.files_liststore.append((nr, str(path)))

    def __files_list_length(self):
        return len(self.window.files_liststore)

    def __get_file_path(self, file_index):
        return self.window.files_liststore[file_index][1]

    # Sprawdzanie plików

    def __video_path_valid(self, path):
        extension = path.split(sep=".")[1]
        return extension.lower() == "avi"

    def __database_path_valid(self, path):
        extension = path.split(sep=".")[1]
        return extension.lower() == "db"

    # Włączanie/wyłączanie przycisków

    def __play_button_enable(self, value=True):
        self.window.play_button.set_sensitive(value)

    def __pause_button_enable(self, value=True):
        self.window.pause_button.set_sensitive(value)

    def __stop_button_enable(self, value=True):
        self.window.stop_button.set_sensitive(value)

    def __replay_button_enable(self, value=True):
        self.window.replay_button.set_sensitive(value)

    def __open_files_button_enable(self, value=True):
        self.window.open_file_button.set_sensitive(value)

    def __enable_main_menu(self, value=True):
        self.window.open_file_button.set_sensitive(value)
        self.window.open_database_button.set_sensitive(value)
        self.window.open_images_button.set_sensitive(value)
        self.window.delete_files_button.set_sensitive(value)
        self.window.settings_button.set_sensitive(value)
        self.window.documentation_button.set_sensitive(value)
        self.window.about_button.set_sensitive(value)

    def clear_main_image(self):
        self.window.main_image.set_from_file(".test.jpg")

    # Głowna pętla przetwarzania obrazu

    def algorithm(self):
        if self.__exit_flag:
            return False

        if self.__play_file_flag:

            if self.__input_video is None:
                path = self.__get_file_path(self.__played_file)
                Algorithm.set_file(path)
                self.__input_video = VideoReader(path)
                self.__current_frame_index = 1

            frame = Frame(self.__input_video)
            self.window.files_treeview.set_cursor(self.__played_file)

            if not self.__input_video.is_good():
                # Zresetuj dane przechowywane przez algorytm przed otwarciem nowego pliku
                Algorithm.reset()
                if (self.__played_file + 1) < self.__files_list_length():
                    # Pobierz następny plik do przetwarzania
                    self.__current_frame_index = 1
                    self.__played_file += 1
                    path = self.__get_file_path(self.__played_file)
                    self.window.files_treeview.set_cursor(self.__played_file)
                    self.__input_video = VideoReader(path)
                    Algorithm.set_file(path)
                else:
                    # Zakończ odtwarzanie jeśli nie ma żadnych plików
                    self.__play_file_flag = False
                    self.__played_file = 0
                    self.__open_files_button_enable(True)
                    self.__play_button_enable(True)
                    self.__pause_button_enable(False)
                    self.__stop_button_enable(False)
                    self.__replay_button_enable(False)
                    self.__input_video = None
                    self.__enable_main_menu(True)
                    self.__write_msg("Koniec")
            else:
                # Konwersja rozmiaru
                frame = Algorithm.resize(frame)

                # Krok algorytmu
                frame, mask, records = Algorithm.perform(frame, self.database, self.img_saver, self.__run_alg_flag)

                # Nagrywanie wyniku
                if self.__record_video_flag:
                    # Stwórz wynikowy plik wideo
                    if self.__output_video is None:
                        size = self.__input_video.size()
                        self.__output_video = VideoWriter(size)
                    # Zapisz klatkę obrazu
                    self.__output_video.write(frame.img)

                # Dodanie wyniku do listview
                self.__add_result_to_list(records, self.__get_file_path(self.__played_file))

                # Zapisz klatkę obrazu do tymczasowego pliku
                if not self.__display_mask_flag:
                    self.__save_image(frame.img)
                else:
                    self.__save_image(mask)

                # Zamień plik na pixbuf
                pixbuf = self.__conver_image_to_pixbuf()
                self.window.main_image.set_from_pixbuf(pixbuf)
                self.__write_current_number()
                self.__current_frame_index += 1
        return True

    # Metody pomocnicze

    def __add_result_to_list(self, cars_data, path):
        if len(cars_data):
            for record in cars_data:
                nr = self.__record_index
                width = "%2.2f m" % record["width"]
                height = "%2.2f m" % record["height"]
                area = "%2.2f m2" % record["area"]
                speed = "%2.2f km/h" % record["speed"]
                color = "R:%sG:%sB:%s" % (str(record["color"][0]), str(record["color"][1]), str(record["color"][2]))
                self.window.detected_cars_liststore.append((nr, width, height, area, speed, color, path))
                self.__record_index += 1

    def __run_file_chooser_dialog(self, name, allow_multiple=True):
        # Stwórz okno
        action = Gtk.FileChooserAction.OPEN
        buttuons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        file_chooser_dialog = Gtk.FileChooserDialog(name, None, action,buttuons)
        file_chooser_dialog.set_select_multiple(allow_multiple)
        response = file_chooser_dialog.run()

        # Sprawdź zwrócony wynik
        result = None if response != Gtk.ResponseType.OK else file_chooser_dialog.get_filenames()

        # Zniszcz okno
        file_chooser_dialog.destroy()

        return result

    def __save_image(self, image):
        cv2.imwrite(WindowController.tmp_images_directory+"/"+str(self.__current_frame_index)+".jpg", image)

    def __write_msg(self, txt):
        self.window.write_on_statusbar(txt)

    def __write_current_number(self):
        # self.__write_msg("Przetwarzanie klatki nr "+str(self.__current_frame_index))
        fraction = float(self.__current_frame_index) / float(self.__input_video.frames_count())
        self.window.progressbar.set_fraction(fraction)

    def __preprare_directory(self):
        if os.path.isdir(WindowController.tmp_images_directory):
            shutil.rmtree(WindowController.tmp_images_directory)
        os.mkdir(WindowController.tmp_images_directory)

    def __conver_image_to_pixbuf(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(WindowController.tmp_images_directory+"/"+str(self.__current_frame_index)+".jpg")
        return pixbuf
