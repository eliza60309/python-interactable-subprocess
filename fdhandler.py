import threading
import queue

class reader(threading.Thread):
    '''
    usage:
        psudo_fd = reader(pipe)
        psudo_fd.start()
        string = psudo_fd.read()
        psudo_fd.join()

    helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd):
        assert callable(fd.read)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue.Queue()

    def run(self):
        '''the body of the thread: read lines and put them on the queue.'''
        while True:
            char = self._fd.read(1)
            self._queue.put(char)


    def eof(self):
        '''check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()
    
    def empty(self):
        '''check whether the queue is empty.'''
        return self._queue.empty()

    def read(self):
        '''reads from the queue'''
        string = ""
        while not self._queue.empty():
            string += self._queue.get().decode()
        print(string)
        return string

class writer():
    '''
    usage:
        psudo_fd = writer(pipe)
        psudo_fd.write("hey")

    '''
    def __init__(self, fd):
        assert callable(fd.write)
        assert callable(fd.flush)
        self._fd = fd
        
    def write(self, string):
        '''writes to the file descriptor'''
        self._fd.write(string.encode())
        self._fd.flush()

class fdhandler():
    '''
    usage:
        fd = fdhandler(readable_fd, writable_fd)
        string = fd.read()
        fd.write("hey")
    '''
    def __init__(self, read_fd, write_fd):
        self._read_fd = reader(read_fd)
        self._write_fd = writer(write_fd)
        self._read_fd.start()
    
    def empty(self):
        return self._read_fd.empty()
    
    def eof(self):
        return self._read_fd.eof()
    
    def join(self):
        self._read_fd.join()
    
    def read(self):
        return self._read_fd.read()
    
    def write(self, string):
        self._write_fd.write(string)

if __name__ == "__main__":
    pass