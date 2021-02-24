from yaps.api import BaseConnection, protocol


class Publish(BaseConnection):

    def __init__(self, ip: str, port: int, flags=None):
        super().__init__(ip, port)

    async def start(self, topic: str, message: str) -> bool:
        # Send: Publish
        await self.open()
        await self.send(protocol.Commands.PUBLISH)

        # Receive: Publish ACK
        packet = await self.read()
        if not await protocol.cmd_ok(packet, protocol.Commands.PUBLISH_ACK,
                                     self._writer):
            return False

        # Send: Publish + Data
        data = f'{topic} | {message}'.encode('utf-8')
        await self.send(protocol.Commands.PUBLISH, data=data)

        # Receive: Publish OK
        pub_ack = await self.read()
        if not await protocol.cmd_ok(pub_ack, protocol.Commands.PUBLISH_OK):
            return False

        await self.close()

        return True
