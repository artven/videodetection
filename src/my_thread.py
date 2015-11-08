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

