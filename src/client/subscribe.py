from api.base_connection import BaseConnection
from api import protocol
from utils.config import Config
from utils.log import Log


class Subscribe(BaseConnection):

    def __init__(self, topic: str, ip=None, port=None, flags=None):
        ip = Config.get()['client']['ip'] if ip is None else ip
        port = Config.get()['client']['port'] if port is None else port
        self.topic = topic
        super().__init__(ip, port)

    async def start(self):
        await self.open()

        await self.send(protocol.Commands.SUBSCRIBE)

        response = await self.read()
        if not self._cmd_ok(response, protocol.Commands.SUBSCRIBE_ACK):
            return

        topic = self.topic.encode('utf-8')
        await self.send(protocol.Commands.SUBSCRIBE, data=topic)

        Log.info(f'Subscribed to "{self.topic}"')

        await self.close()
