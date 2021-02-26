from yaps.client.publish import Publish
from yaps.client.subscribe import Subscribe
from yaps.utils import Log


class Client:

    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port
        Log.init(server=False)

    def subscribe(self, topic: str, data_received: callable = None) -> None:
        """ Throws ConnectionRefusedError. """
        sub = Subscribe(self._ip, self._port, data_received)

        Log.info(f'[Client] Subscribing to "{topic}"')
        sub.start(topic)

    def publish(self, topic: str, message: str) -> bool:
        """
            Returns if the publish is succesful or not.
            Throws ConnectionRefusedError.
        """
        publish = Publish(self._ip, self._port)
        try:
            pub_ok = publish.start(topic, message)
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
