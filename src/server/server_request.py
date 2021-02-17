import asyncio

from subscription import Subscription
from publication import Publication
from api import protocol
from api.packet import Packet
from utils.log import Log


class Request:

    def __init__(self, reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer

    async def respond(self):
        packet = await protocol.read_packet(self._reader)

        if packet.cmd == protocol.Commands.PUBLISH:
            await self._handle_publish()
        elif packet.cmd == protocol.Commands.SUBSCRIBE:
            await self._handle_subscribe()
        else:
            await self._handle_wrong_cmd()

    async def _handle_publish(self) -> Publication:
        Log.debug('[Server] Pub')
        # Publish ACK
        await protocol.send_packet(self._writer, protocol.Commands.PUBLISH_ACK)

        # Publish 'message' to 'topic'
        packet = await protocol.read_packet(self._reader)
        if not await protocol.cmd_ok(packet, protocol.Commands.PUBLISH,
                                     self._writer):
            return

        data = packet.data.decode('utf-8')

        # Ensure publish is OK according to the format required.
        if not protocol.publish_ok(data):
            Log.debug(f'[Server] Pub -> Publish "{data}" is incorrect format.')
            return None

        Log.debug(f'[Server] Pub -> {data}')

        # Publish OK
        await protocol.send_packet(self._writer, protocol.Commands.PUBLISH_OK)

        topic, message = protocol.get_topic_and_msg(data)
        return Publication(topic, message)

    async def _handle_subscribe(self) -> Subscription:
        Log.debug('[Server] Sub')

        # Subscribe ACK
        await protocol.send_packet(self._writer,
                                   protocol.Commands.SUBSCRIBE_ACK)

        # Subscribe 'topic'
        packet = await protocol.read_packet(self._reader)
        if not await protocol.cmd_ok(packet, protocol.Commands.SUBSCRIBE,
                                     self._writer):
            return None

        topic = packet.data.decode('utf-8')

        # Ensure topic is OK according to the format required.
        if not protocol.topic_ok(topic):
            Log.debug(f'[Server] Sub -> Topic "{topic}" is incorrect format.')
            return None

        Log.debug(f'[Server] Sub -> Topic: "{topic}"')

        # Subscribe OK
        await protocol.send_packet(self._writer,
                                   protocol.Commands.SUBSCRIBE_OK)

        return Subscription(topic, self._reader, self._writer)

    async def _handle_wrong_cmd(self):
        Log.debug('[Server] Wrong cmd')

