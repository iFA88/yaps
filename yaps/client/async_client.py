from yaps.client.async_subscribe import AsyncSubscribe
from yaps.client.async_publish import AsyncPublish
from yaps.utils.log import Log


class AsyncClient:

    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port
        Log.init(server=False)

    async def subscribe(self, topic: str,
                        data_received: callable = None) -> None:
        """ Throws ConnectionRefusedError. """
        sub = AsyncSubscribe(self._ip, self._port, data_received)

        Log.info(f'[Client] Subscribing to "{topic}"')
        await sub.start(topic)

    async def publish(self, topic: str, message: str) -> bool:
        """
            Returns if the publish is succesful or not.
            Throws ConnectionRefusedError.
        """
        publish = AsyncPublish(self._ip, self._port)
        try:
            pub_ok = await publish.start(topic, message)
        except ConnectionRefusedError:
            Log.err(f'[Client ]Failed to connect to server {self._ip} '
                    f'on port {self._port}')
            return

        if pub_ok:
            Log.info(f'[Client] Published "{message}" to topic "{topic}"')
        else:
            Log.info(f'[Client] Failed to publish "{message}" to'
                     f' topic "{topic}"')

        return pub_ok
