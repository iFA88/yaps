from yaps.api import protocol
from yaps.client.async_base_connection import AsyncBaseConnection
from yaps.utils import Log


class AsyncPublish(AsyncBaseConnection):

    def __init__(self, ip: str, port: int, flags=None):
        super().__init__(ip, port)

    async def start(self, topic: str, message: str) -> bool:
        success = True

        try:
            # Send: Publish
            await self.open()
            await self.send(protocol.Commands.PUBLISH)

            # Receive: Publish ACK
            packet = await self.read()
            if not await protocol.async_cmd_ok(packet,
                                               protocol.Commands.PUBLISH_ACK,
                                               self._writer):
                success = False

            if success:
                # Send: Publish + Data
                data = f'{topic} | {message}'.encode('utf-8')
                await self.send(protocol.Commands.PUBLISH, data=data)

                # Receive: Publish OK
                pub_ack = await self.read()
                if not await protocol.async_cmd_ok(pub_ack,
                                                   protocol.Commands.PUBLISH_OK): # noqa
                    success = False

        except Exception as e:
            Log.debug(f'Unknown error: {e}')

        finally:
            await self.close()

        return success
