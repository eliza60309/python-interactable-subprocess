from http.server import BaseHTTPRequestHandler as session

class GetHandler(session):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = """
        <html>
            <head>
                <title>Title goes here!</title>
            </head>
            <body>
                <p>This is a test.</p>
            </body>
        </html>
        """
        self.wfile.write(response.encode())
        
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 5566), GetHandler)
    print('Port is 5566')
    server.serve_forever()
