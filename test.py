__author__ = 'rafal'

from os import listdir
from datetime import datetime
from numpy import mean, median

# do testowania
from src.video import VideoReader, Frame
from src.alg import Algorithm
from src.config import Configuration
from src.logs import Database, ImageSaver, Logger
import cv2

# plik zawierający dane wejściowe
input_file = open("input.txt")

# plik do zapisu wyników
output_file = open("output.txt", "w")

# folder zawierający pliki avi
folder = "/media/Dane/Dropbox/Studia/IV rok/inżynierka/Dane_AVI"
avi_files = listdir("/media/Dane/Dropbox/Studia/IV rok/inżynierka/Dane_AVI")

# zapisywanie wyników
db = Database()
img_saver = ImageSaver()

used_files_count = 0
unused_files_count = 0
not_found_files_count = 0
valid_detection_count = 0
bad_detection_count = 0
speed_errors = []
length_errors = []

Logger.start()
Configuration.load_config()


def test_sigle_file(file):
    Algorithm.file = file
    Algorithm.reset()
    input_video = VideoReader(file)
    result = []

    while 1:
        frame = Frame(input_video)

        if not input_video.is_good():
            break

        frame = Algorithm.resize(frame)
        frame, mask, records = Algorithm.perform(frame, db, img_saver, True)

        if records is not None and len(records) > 0:
            for rec in records:
                result.append((round(rec['width'], 2), round(rec["speed"], 2)))

    return result

form = "%5s %10s %10s %20s %20s %10s %10s %10s %10s %10s %10s %20s \n"
columns = ("lp", "dlugosc", "prędkosć", "plik orginalny", "plik znaleziony", "dlugosc", "błąd", "błąd %",
           "prędkość", "błąd", "błąd %", "status")
output_file.write(form % columns)

t1 = datetime.now().replace(microsecond=0)

for i, line in enumerate(input_file.readlines()):
    data = line.split(sep="\t")
    lp, date, time, speed, lenght, axes = str(i), data[0], data[1], data[3], data[4], data[5]
    HH, MM, SS = time.split(sep=":")[0], time.split(sep=":")[1], time.split(sep=":")[2]
    orginal_file = "M151001_"+HH+MM+SS+".avi"
    if float(speed) > 0 and float(lenght) > 0 and int(axes) in (1, 2):
        found_file = None
        for SS2 in range(int(SS)-2, int(SS)+3):
            s = str(SS2) if len(str(SS2)) > 1 else "0"+str(SS2)
            f = "M151001_"+HH+MM+s+".avi"
            if f in avi_files:
                found_file = f
                used_files_count += 1
                results = test_sigle_file(folder+"/"+f)
                for r in results:
                    found_length, found_speed = r[0], r[1]

                    # błąd długości
                    length_error = abs(float(lenght) - found_length)
                    length_error = round(length_error, 2)
                    length_error_pr = round((length_error / float(lenght)), 2) * 100
                    length_errors.append(length_error_pr)

                    # błąd prędkości
                    speed_error = abs(float(speed) - found_speed)
                    speed_error = round(speed_error, 2)
                    speed_error_pr = round((speed_error / float(speed)), 2) * 100
                    speed_errors.append(speed_error_pr)

                    if speed_error_pr < 30 and length_error_pr < 30:
                        status = "OK"
                        valid_detection_count += 1
                    else:
                        status = "BAD"
                        bad_detection_count += 1

                    output_file.write(form % (lp, lenght, speed, orginal_file, found_file,
                                              str(found_length), str(length_error), str(length_error_pr),
                                              str(found_speed), str(speed_error), str(speed_error_pr), status))
                break
        if found_file is None:
            not_found_files_count += 1
            status = "nie znaleziono pliku"
            print("%4d - nie znaleziono pliku" % i)
            output_file.write("%5s %10s %10s %20s %20s \n" % (lp, lenght, speed, orginal_file, status))
        else:
            print("%4d - przeprowadzono analizę " % i)
    else:
        unused_files_count += 1
        status = "niepoprawny pomiar"
        print("%4d - niepoprawny pomiar" % i)
        output_file.write("%5s %10s %10s %20s %20s \n" % (lp, lenght, speed, orginal_file, status))

input_file.close()
output_file.close()

print("wpisy poprawne " + str(used_files_count))
print("wpisy bez pliku " + str(not_found_files_count))
print("wpisy nie poprawne " + str(unused_files_count))
print("prawidłowa detekcja " + str(valid_detection_count))
print("błędna detekcja " + str(bad_detection_count))

print("błędy:")
print("długość - błąd średni: " + str(mean(length_errors)))
print("długość - mediana błędu: " + str(median(length_errors)))
print("prędkość - błąd średni: " + str(mean(speed_errors)))
print("prędkość - mediana błędu: " + str(median(speed_errors)))

t2 = datetime.now().replace(microsecond=0)
print(t2-t1)