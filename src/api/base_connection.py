import asyncio

from api import protocol
from api.packet import Packet
from utils.log import Log
from utils.config import Config


class BaseConnection:

    def __init__(self,
                 ip=Config.get()['server']['ip'],
                 port=Config.get()['server']['port']):
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

    def _cmd_ok(self, packet: Packet, cmd: int) -> bool:
        ok = True
        if packet is None:
            Log.err('Failed to read packet!')
            ok = False
        elif packet.cmd != cmd:
            Log.err('Packet command incorrect!')
            ok = False

        return ok