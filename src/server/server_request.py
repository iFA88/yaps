import asyncio

from api import protocol
from api.packet import Packet
from utils.log import Log


class State:
    START = 0
    PING_PONG = 1
    PING_PONG_1_MISS = 2
    PING_PONG_2_MISS = 2


class Request:

    def __init__(self, reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer
        self._state = State.START

    async def respond(self):
        packet = await protocol.read_packet(self._reader)

        if self._state == State.START:
            if packet.cmd == protocol.Commands.PUBLISH:
                await self._handle_publish()
            elif packet.cmd == protocol.Commands.SUBSCRIBE:
                await self._handle_subscribe()
            else:
                await self._handle_wrong_cmd()
        elif self._state == State.PING_PONG:
            pass
        elif self._state == State.PING_PONG_1_MISS:
            pass
        elif self._state == State.PING_PONG_2_MISS:
            pass

    async def _handle_publish(self) -> str:
        Log.debug('[Server] Pub')
        # Publish ACK
        await protocol.send_packet(self._writer, protocol.Commands.PUBLISH_ACK)

        # Publish 'message' to 'topic'
        packet = await protocol.read_packet(self._reader)

        if not await self._cmd_ok(packet, protocol.Commands.PUBLISH):
            return

        # TODO: Ensure publish is OK?
        data = packet.data.decode('utf-8')

        Log.debug(f'[Server] Pub -> {data}')

        # Publish OK
        await protocol.send_packet(self._writer, protocol.Commands.PUBLISH_OK)
        return data

    async def _handle_subscribe(self) -> str:
        Log.debug('[Server] Sub')

        # Subscribe ACK
        await protocol.send_packet(self._writer,
                                   protocol.Commands.SUBSCRIBE_ACK)

        # Subscribe 'topic'
        packet = await protocol.read_packet(self._reader)

        if not await self._cmd_ok(packet, protocol.Commands.SUBSCRIBE):
            return

        # TODO: Ensure subscription is OK?
        data = packet.data.decode('utf-8')

        Log.debug(f'[Server] Sub -> {data}')

        # Publish OK
        await protocol.send_packet(self._writer,
                                   protocol.Commands.SUBSCRIBE_OK)
        # Change state and return the data
        self._state = State.PING_PONG
        return data

    async def _handle_wrong_cmd(self):
        Log.debug('[Server] Wrong cmd')

    async def _cmd_ok(self, packet: Packet, cmd: int) -> bool:
        """
            Returns true if command is okay, and sends a BAD_CMD packet
            if the command is not okay.
        """
        ok = True
        if packet is None:
            Log.err('Failed to read packet!')
            ok = False
        elif packet.cmd != cmd:
            Log.err('Packet command incorrect!')
            await protocol.send_packet(self._writer, protocol.Commands.BAD_CMD)
            ok = False

        return ok
