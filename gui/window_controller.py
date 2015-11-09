__author__ = 'rafal'

import os
import shutil
import cv2

from src.video import VideoReader, VideoWriter
from gi.repository import Gtk, GdkPixbuf, GLib
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
        self.__output_video = None
        self.__record = False
        self.__loaded_frames = 0
        self.__current_frame_index = 1

        self.database = Database()
        self.img_saver = ImageSaver()
        GLib.timeout_add(50, self.algorithm)
        #self.algorithm_thread = MyThread(self.algorithm)
        #self.algorithm_thread.start()

    def algorithm(self):
        if self.exit_flag:
            return False

        if self.play_file_flag:
            print(self.__current_frame_index)
            frame = Frame(self.__input_video)

            if not self.__input_video.is_good():
                self.play_file_flag = False
                self.window.disable_buttons()
                self.__write_msg("Koniec")
            else:
                frame = perform(frame, self.database, self.img_saver)
                if self.__record:
                    self.__output_video.write(frame.img)

                self.__save_image(frame.img)
                pixbuf = self.__conver_image_to_pixbuf()
                self.window.main_image.set_from_pixbuf(pixbuf)
                self.__write_current_number()
                self.__current_frame_index += 1
        return True

    def set_new_file(self, path):
        self.__path = path
        self.new_file_flag = True
        self.__input_video = VideoReader(self.__path)

    def play_file(self):
        if self.new_file_flag:
            self.window.write_on_statusbar("Przygotowywanie katalogu...")
            self.__preprare_directory()
            self.new_file_flag = False
        self.play_file_flag = True

    def stop_playing(self):
        self.__path = None
        self.play_file_flag = False

    def pause_playing(self):
        self.play_file_flag = False

    def open_images(self):
        images_list = os.listdir('images')
        if len(images_list):
            os.system("eog " + "images/")

    def delete_old_items(self):
        shutil.rmtree('images')
        shutil.rmtree('data')
        os.mkdir('images')
        os.mkdir('data')

    def set_recording(self, value):
        if value:
            if self.__output_video is None:
                size = self.__input_video.size()
                self.__output_video = VideoWriter(size)
            self.__record = value

    def set_algorithm(self, value):
        Configuration.run_alg = value

    def set_direction_r2l(self):
        Configuration.direction("right2left")
        Configuration.save_config()

    def set_direction_l2r(self):
        Configuration.direction("left2right")
        Configuration.save_config()

    def exit(self):
        self.exit_flag = True

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

    def __conver_image_to_pixbuf(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(WindowController.tmp_images_directory+"/"+str(self.__current_frame_index)+".jpg")
        return pixbuf
