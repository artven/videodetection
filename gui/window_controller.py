__author__ = 'rafal'

import os
import shutil
import cv2
import time
from src.video import VideoReader
from src.my_thread import MyThread
from gi.repository import Gtk, GdkPixbuf
from src.logs import Database, ImageSaver
from src.alg import perform
from src.video import Frame
from src.config import Configuration

class WindowController:

    tmp_images_directory = "/tmp/loaded_file"

    def __init__(self, window):
        self.window = window

        self.new_file_flag = False
        self.play_file_flag = False
        self.exit_flag = False

        self.__path = None
        self.__input_video = None
        self.__loaded_frames = 0
        self.__current_frame_index = 1

        self.algorithm_thread = MyThread(self.algorithm)

        # Wystartuj wszystkie wątki
        self.run_threads()

    def algorithm(self):
        database = Database()
        img_saver = ImageSaver()
        while not self.exit_flag:
            if self.play_file_flag:
                print(self.__current_frame_index)
                frame = Frame(self.__input_video)

                if not self.__input_video.is_good():
                    self.play_file_flag = False
                    self.window.disable_buttons()
                    self.__write_msg("Koniec")
                    continue

                # TODO jeżeli algorytm działa
                frame = perform(frame, database, img_saver)
                self.__save_image(frame.img)
                pixbuf = self.__conver_image_to_pixbuf()
                self.window.main_image.set_from_pixbuf(pixbuf)
                self.__write_current_number()
                self.__current_frame_index += 1

                # opóźnienie odtwarzania
                time.sleep(Configuration.play_delay())

    def run_threads(self):
        self.algorithm_thread.start()

    def exit(self):
        self.exit_flag = True

    def set_new_file(self, path):
        self.__path = path
        self.new_file_flag = True

    def play_file(self):
        if self.new_file_flag:
            self.window.write_on_statusbar("Przygotowywanie katalogu...")
            self.__preprare_directory()
            self.__input_video = VideoReader(self.__path)
            self.new_file_flag = False
        self.play_file_flag = True

    def stop(self):
        self.__path = None
        self.play_file_flag = False

    def pause_playing(self):
        self.play_file_flag = False

    def __save_image(self, image):
        cv2.imwrite(WindowController.tmp_images_directory+"/"+str(self.__current_frame_index)+".jpg", image)

    def __write_msg(self, txt):
        self.window.write_on_statusbar(txt)

    def __write_current_number(self):
        self.__write_msg("Przetwarzanie "+str(self.__current_frame_index)+"/"+str(self.__input_video.frames_count()))

    def __preprare_directory(self):
        if os.path.isdir(WindowController.tmp_images_directory):
            shutil.rmtree(WindowController.tmp_images_directory)
        os.mkdir(WindowController.tmp_images_directory)

    def __load_videofile(self, path):
        input_video = VideoReader(path)
        frames_count = int(input_video.frames_count())
        i = 1
        while 1:
            image = input_video.read()
            if not input_video.is_good():
                break
            cv2.imwrite(WindowController.tmp_images_directory+"/"+str(i)+".jpg", image)
            self.window.write_on_statusbar("Wczytywano... " + str(i)+"/"+str(frames_count))
            i += 1
        self.__loaded_frames = i
        self.__current_frame_index = 1
        self.window.enable_buttons()

    def __conver_image_to_pixbuf(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(WindowController.tmp_images_directory+"/"
                                                + str(self.__current_frame_index)+".jpg")
        return pixbuf
