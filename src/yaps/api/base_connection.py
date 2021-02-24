import asyncio

from yaps.api import protocol
from yaps.utils.log import Log


class BaseConnection:

    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port
        self._reader = None
        self._writer = None

    async def send(self, cmd: int, flags: int = 0, data: bytes = b''):
        if self._writer is not None:
            await protocol.send_packet(self._writer, cmd, flags, data)

    async def read(self):
        if self._reader is not None:
            return await protocol.read_packet(self._reader)

    async def open(self):
        self._reader, self._writer = await asyncio.open_connection(
                                                self._ip,
                                                self._port)
        Log.debug(f'Connecting to {self._ip}:{self._port}')

    async def close(self):
        if self._writer is not None:
            self._writer.close()
            await self._writer.wait_closed()
