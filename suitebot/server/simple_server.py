from socket import socket
from time import time

from suitebot.server.simple_request_handler import SimpleRequestHandler

SHUTDOWN_REQUEST = "EXIT"
UPTIME_REQUEST = "UPTIME"


class SimpleServer(object):
    _should_shut_down = False
    _start_timestamp = 0

    def __init__(self, port: int, request_handler: SimpleRequestHandler) -> None:
        self._port = port
        self._request_handler = request_handler

    def run(self) -> None:
        self._start_timestamp = time()
        sock = socket()
        try:
            sock.bind(('', self._port))
            sock.listen()
            while not self._should_shut_down:
                connection, address = sock.accept()
                try:
                    self._handle_request(connection)
                finally:
                    connection.close()                
        finally:
            sock.close()

    def _handle_request(self, connection: socket) -> None:
        request = connection.makefile().readline().strip()
        if not request:
            return
        if request == SHUTDOWN_REQUEST:
            self._should_shut_down = True
            return
        if request == UPTIME_REQUEST:
            connection.sendall(str(int(time() - self._start_timestamp)).encode('utf'))
        else:
            connection.sendall(self._request_handler.process_request(request).encode('utf'))
