from api.base_connection import BaseConnection
from api import protocol
from utils.config import Config
from utils.log import Log


class Publish(BaseConnection):

    def __init__(self, topic, message, ip=None, port=None, flags=None):
        ip = Config.get()['client']['ip'] if ip is None else ip
        port = Config.get()['client']['port'] if port is None else port
        self.topic = topic
        self.message = message
        super().__init__(ip, port)

    async def start(self):
        await self.open()

        await self.send(protocol.Commands.PUBLISH)

        response = await self.read()
        if not self._cmd_ok(response, protocol.Commands.PUBLISH_ACK):
            return

        data = f'{self.topic} | {self.message}'.encode('utf-8')
        await self.send(protocol.Commands.PUBLISH, data=data)

        Log.info(f'Published "{self.message}" to topic "{self.topic}"')

        await self.close()