import socket
import io

from yaps.api import protocol, Packet
from yaps.utils.log import Log
from yaps.utils.log_user import BasicLogUser


class BaseConnection(BasicLogUser):

    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port
        self._sock = None
        self._writer: io.BufferedWriter = None
        self._reader: io.BufferedReader = None

    def send(self, cmd: int, flags: int = 0, data: bytes = b''):
        if self._writer is not None:
            protocol.send_packet(self._writer, cmd, flags, data)

    def read(self) -> Packet:
        if self._reader is not None:
            return protocol.read_packet(self._reader)

    def open(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._ip, self._port))
        self._writer = self._sock.makefile('wb')
        self._reader = self._sock.makefile('rb')
        Log.debug(f'Connecting to {self._ip}:{self._port}')

    def close(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None
