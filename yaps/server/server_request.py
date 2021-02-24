import asyncio

from yaps.server.subscription import Subscription
from yaps.server.publication import Publication
from yaps.api import protocol
from yaps.utils.log import Log


class RequestResult:
    """ Wrapper class for result. """
    def __init__(self, result):
        self.data = result

    def __repr__(self):
        return str(self.data)

    def __eq__(self, other):
        return type(self.data) == other


class Request:
    """
        Handles a new tcp request and returns the appropiate result.
        This class is invoked by the server upon a new request
        and should not be used directly.
    """

    def __init__(self, reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer

    async def respond(self) -> RequestResult:
        packet = await protocol.read_packet(self._reader)
        result = None

        if packet is None:
            result = await self._handle_wrong_cmd()
        elif packet.cmd == protocol.Commands.PUBLISH:
            result = await self._handle_publish()
        elif packet.cmd == protocol.Commands.SUBSCRIBE:
            result = await self._handle_subscribe()

        return RequestResult(result)

    async def _handle_publish(self) -> Publication:
        # Log.debug('Server: PUB')
        # Send: Publish ACK
        await protocol.send_packet(self._writer, protocol.Commands.PUBLISH_ACK)

        # Receive: Publish + Data ('topic' | 'message')
        packet = await protocol.read_packet(self._reader)
        if not await protocol.cmd_ok(packet, protocol.Commands.PUBLISH,
                                     self._writer):
            return

        data = packet.data.decode('utf-8')

        # Ensure publish is OK according to the format required.
        if not protocol.publish_ok(data):
            Log.debug(f'[Server] Pub -> Publish "{data}" is incorrect format.')
            await protocol.send_packet(self._writer,
                                       protocol.Commands.INCORRECT_FORMAT)
            return None

        # Publish OK
        await protocol.send_packet(self._writer, protocol.Commands.PUBLISH_OK)

        topic, message = protocol.get_topic_and_msg(data)
        publication = Publication(topic, message)

        Log.info(f'[Server] New Pub: "{publication}"')

        return publication

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
