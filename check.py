import sys
import subprocess
import time
import threading
import queue as Queue
import os
import cgi
from http.server import BaseHTTPRequestHandler as session

        


class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

class main_thread(threading.Thread):
    def run(self):
        consume(['a.exe'])

def consume(command):
    global program_i
    global program_o
    '''
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    '''

    # Launch the command as subprocess.
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout_queue = Queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = Queue.Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()

    # Check the queues if we received some output (until there is nothing more to get).
    while not stdout_reader.eof() or not stderr_reader.eof():
        # Show what we received from standard output.
        while not stdout_queue.empty():
            line = stdout_queue.get()
            program_o.put(line)
        # Show what we received from standard error.
        while not stderr_queue.empty():
            line = stderr_queue.get()
            program_o.put(line)
        while not program_i.empty():
            line = program_i.get()
            if(line == None):
                continue
            line += "\r\n"
            process.stdin.write(line.encode())
            process.stdin.flush()
        # Sleep a bit before asking the readers again.
        time.sleep(.1)

    # Let's be tidy and join the threads we've started.
    stdout_reader.join()
    stderr_reader.join()

    # Close subprocess' file descriptors.
    process.stdout.close()
    process.stderr.close()
ans = ""
class Handler(session):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        if(self.path != "/"):
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        global ans
        while not program_o.empty():
            ans += str(program_o.get()) + "<br>"
        response = """
        <html>
            <body>
                <form method="post">
                    <input type="text" name="input"/>
                    Program returns:<br>
                    <p id="console">%s</p>
                </form>
            </body>
        </html>
        """ % ans
        self.wfile.write(response.encode())

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        program_i.put(form.getvalue("input"))
        global ans
        while not program_o.empty():
            ans += str(program_o.get()) + "<br>"
        response = """
        <html>
            <body>
                <form method="post">
                    <input type="text" name="input"/><br>
                    Program returns:<br>
                    <p id="console">%s</p>
                </form>
            </body>
        </html>
        """ % ans
        self.wfile.write(response.encode())

program_i = Queue.Queue()
program_o = Queue.Queue()
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8888), Handler)
    print('Port is 8888')
    ms = main_thread()
    ms.start()
    server.serve_forever()