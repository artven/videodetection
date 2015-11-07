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



'''
exitFlag = 0


def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            thread_name.exit()
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1


class MyThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting " + self.name)



# Create new threads
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")
'''