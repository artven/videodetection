__author__ = 'rafal'


import threading
import time
import functools


class MyThread (threading.Thread):

    id = 1

    def __init__(self,  fun, *args):
        threading.Thread.__init__(self)
        self.thread_id = MyThread.id
        MyThread.id += 1
        self.name = "thread" + str(self.thread_id)
        self.function = functools.partial(fun, *args)
        self.exit_flag = False

    def run(self):
            self.function()



if __name__ == "__main__":

    def f(arg1, arg2):
        while 1:
            print(arg1 + arg2)
            time.sleep(1)

    thread1 = MyThread(f, "hello world", "witaj swiecie")
    thread2 = MyThread(f, "adam giza", "mi ubliza")

    thread1.start()
    thread2.start()

