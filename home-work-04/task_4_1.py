from threading import current_thread, Lock, Thread
import time
import random


def worker(file: object, *args):
    """
    worker function writes two strings with random pause to
    shared file using synchronization primitive
    :param file: file-object
    :return:
    """
    thread_name = current_thread().name
    lock.acquire()
    file.write(thread_name + ': ' + 'started.\n')
    time.sleep(random.random() * 5)
    file.write(thread_name + ': ' + 'done.\n')
    lock.release()


if __name__ == '__main__':
    file = open('test.txt', 'a')
    lock = Lock()
    for t in range(10):
        file_thread = Thread(name="thread_{}".format(t), target=worker, args=(file,))
        file_thread.start()
