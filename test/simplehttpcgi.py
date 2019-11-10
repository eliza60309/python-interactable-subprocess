import sys
import subprocess
import time
import threading
import queue as Queue
import os
import cgi
from http.server import BaseHTTPRequestHandler as session
import fdhandler

class main_thread(threading.Thread):
    def run(self):
        consume(['a.exe'])

def consume(command):
    global program_i
    global program_o
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    fd = fdhandler.fdhandler(process.stdout, process.stdin)
    while not fd.eof():
        while not fd.empty():
            line = fd.read()
            program_o.put(line)
        while not program_i.empty():
            line = program_i.get()
            if(line == None):
                continue
            line += "\n"
            process.stdin.write(line.encode())
            process.stdin.flush()
        time.sleep(.1)
    fd.join()
    process.stdout.close()
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
            ans += program_o.get().replace("\n", "<br>")
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
            ans += program_o.get().replace("\n", "<br>")

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