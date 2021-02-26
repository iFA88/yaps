from yaps.api import protocol
from yaps.client.base_connection import BaseConnection
from yaps.utils import Log


class Publish(BaseConnection):

    def __init__(self, ip: str, port: int, flags=None):
        super().__init__(ip, port)

    def start(self, topic: str, message: str) -> bool:
        success = True

        try:
            # Send: Publish
            self.open()
            self.send(protocol.Commands.PUBLISH)

            # Receive: Publish ACK
            packet = self.read()
            if not protocol.cmd_ok(packet, protocol.Commands.PUBLISH_ACK,
                                   self._writer):
                success = False

            if success:
                # Send: Publish + Data
                data = f'{topic} | {message}'.encode('utf-8')
                self.send(protocol.Commands.PUBLISH, data=data)

                # Receive: Publish OK
                pub_ack = self.read()
                if not protocol.cmd_ok(pub_ack, protocol.Commands.PUBLISH_OK):
                    success = False

        except Exception as e:
            Log.debug(f'Unknown error: {e}')

        finally:
            self.close()

        return success
