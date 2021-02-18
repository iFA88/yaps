from client.publish import Publish
from client.subscribe import Subscribe
from utils.log import Log


class Client:

    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port

    async def subscribe(self, topic: str,
                        data_received: callable = None) -> None:
        """ Throws ConnectionRefusedError. """
        sub = Subscribe(self._ip, self._port, data_received)

        Log.info(f'Subscribing to "{topic}"')
        await sub.start(topic)

    async def publish(self, topic: str, message: str) -> bool:
        """
            Returns if the publish is succesful or not.
            Throws ConnectionRefusedError.
        """
        publish = Publish(self._ip, self._port)
        pub_ok = await publish.start(topic, message)

        if pub_ok:
            Log.info(f'Published "{message}" to topic "{topic}"')

        return pub_ok