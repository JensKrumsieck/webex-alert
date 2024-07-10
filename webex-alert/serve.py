from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import signal
from util import log_method

token = ""

class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("=")
        self.send_response(200)
        self.end_headers()
        if len(path) > 1:
            global token
            token = path[1]
            self.send_kill()

    def send_kill(self):
        pid = os.getpid()
        os.kill(pid, signal.SIGINT)

@log_method
def run(handler_class=LoginHandler, port=8080) -> str:
    server_address = ('', port)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    return token
