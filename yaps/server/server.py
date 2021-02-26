import asyncio

from yaps.server.subscription import Subscription
from yaps.server.publication import Publication
from yaps.server.subscription_container import SubscriptionContainer
from yaps.server.server_request import Request, RequestResult
from yaps.utils.config import Config
from yaps.utils.log import Log


NAME = 'YAPS'
TASK_DELAY_PING = 5     # In seconds.
TASK_DELAY_PUB = .5     # In seconds.

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 8999


class Server:

    def __init__(self, ip: str, port: int):
        self._subscriptions = SubscriptionContainer()
        self._publications = asyncio.Queue()
        self._ping_pong_tasks = asyncio.PriorityQueue()

        self._ip = ip
        self._port = port
        Log.init(server=True)

    async def _check_timeouts(self):
        """
            Checks all the subscribers to see if their timer has timed out
            and puts all the timed out ones in the priority queue.
        """
        subs = self._subscriptions.get_all()
        timed_out_subs = filter(lambda sub: sub.timed_out(), subs)
        for sub in timed_out_subs:
            await self._ping_pong_tasks.put(sub)

    async def _make_pings_task(self):
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
            await asyncio.sleep(TASK_DELAY_PING)

    async def _make_publications_task(self) -> None:
        """
            Tasks that runs forever and takes publications from the
            publication queue and sends them to the subscribers.
        """
        while True:
            # Get the next publication from the queue and send it.
            pub = await self._publications.get()
            await self._make_publications(pub)
            self._publications.task_done()

    async def _make_publications(self, publication: Publication) -> None:
        """ Sends the publication to all the subscribers of the topic. """
        subs = self._subscriptions.get(publication.topic)

        for sub in subs.copy():
            try:

                Log.debug(f'[Server] Publishing: {self._publications.qsize()}')
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
            # Add new publication to queue
            await self._publications.put(result.data)

        elif result is None:
            # This should not occur!
            Log.debug('ALERT: Result is None! ')

    async def start(self) -> None:
        """ Starts the server. This method runs forever. """
        server = await asyncio.start_server(self._request_handler,
                                            self._ip, self._port)
        ip, port = server.sockets[0].getsockname()
        Log.info(f'{NAME} Server started at {ip} on port {port}')

        async with server:
            await asyncio.gather(self._make_pings_task(),
                                 self._make_publications_task(),
                                 server.serve_forever())


def get_address():
    try:
        return (Config.get()['server']['ip'],
                Config.get()['server']['port'])
    except (TypeError, KeyError):
        return DEFAULT_IP, DEFAULT_PORT
