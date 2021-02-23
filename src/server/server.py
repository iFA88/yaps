import asyncio

from subscription import Subscription
from publication import Publication
from subscription_container import SubscriptionContainer
from server_request import Request, RequestResult
from utils.config import Config
from utils.log import Log


NAME = 'YAPS'
MAKE_PING_DELAY = 1     # In seconds.


class Server:

    def __init__(self, ip: str, port: int):
        self._subscriptions = SubscriptionContainer()
        self._ping_pong_tasks = asyncio.PriorityQueue()

        self._ip = ip
        self._port = port

    async def _make_pings(self):
        """ Task that sends pings to all subscriptions in the queue.
            All subs in this queue have timed out.
        """
        while True:
            await self._check_timeouts()
            while not self._ping_pong_tasks.empty():
                try:
                    subscriber = await self._ping_pong_tasks.get()
                    if subscriber.is_dead():
                        self._delete_subscription(subscriber)
                    else:
                        await subscriber.ping()

                except (ConnectionResetError, BrokenPipeError):
                    Log.err(f'Connection unexpectedly closed {subscriber}')
                    self._delete_subscription(subscriber)

                finally:
                    # We want to remove the task from the queue regardless
                    # if it fails or completes.
                    self._ping_pong_tasks.task_done()

            # Go idle so other tasks can run.
            await asyncio.sleep(MAKE_PING_DELAY)

    async def _check_timeouts(self):
        """
            Checks all the subscribers to see if their timer has timed out
            and puts all the timed out ones in the priority queue.
        """
        subs = self._subscriptions.get_all()
        timed_out_subs = filter(lambda sub: sub.timed_out(), subs)
        for sub in timed_out_subs:
            self._ping_pong_tasks.put_nowait(sub)

    async def _make_publications(self, publication: Publication) -> None:
        """ Sends the publication to all the subscribers of the topic. """
        subs = self._subscriptions.get(publication.topic)
        for sub in subs.copy():
            try:
                pub_ok = await sub.new_data(publication.message)
                if not pub_ok:
                    self._delete_subscription(sub)
            except RuntimeError:
                # This error is caused: RuntimeError: read() called while
                # another coroutine is already waiting for incoming data.
                # Should not do any harm, so therefore ignored.
                pass

    def _delete_subscription(self, subscription: Subscription) -> None:
        self._subscriptions.delete(subscription)

    async def _add_subscription(self, subscription: Subscription) -> None:
        self._subscriptions.add(subscription)
        Log.debug(f'Total subscribers: {self._subscriptions.get_all()}')
        await subscription.start_idle()

    async def _request_handler(self,
                               reader: asyncio.StreamReader,
                               writer: asyncio.StreamWriter) -> None:
        """ Handles a TCP request. """
        request = Request(reader, writer)
        result: RequestResult = await request.respond()

        if result == Subscription:
            await self._add_subscription(result.data)

        elif result == Publication:
            await self._make_publications(result.data)

        elif result is None:
            Log.debug('ALERT: Result is None! ')

    async def start(self) -> None:
        """ Starts the server. This method runs forever. """
        server = await asyncio.start_server(self._request_handler,
                                            self._ip, self._port)
        ip, port = server.sockets[0].getsockname()
        Log.info(f'{NAME} Server started at {ip} on port {port}')

        async with server:
            await asyncio.gather(self._make_pings(),
                                 server.serve_forever())


if __name__ == '__main__':
    Log.init()
    server = Server(Config.get()['server']['ip'],
                    Config.get()['server']['port'])
    asyncio.run(server.start())
