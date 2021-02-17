import asyncio

from subscription import Subscription
from publication import Publication
from subscription_container import SubscriptionContainer
from server_request import Request
from utils.config import Config
from utils.log import Log


MAKE_PING_DELAY = 1     # In seconds.


class Server:

    def __init__(self):
        self._sub_container = SubscriptionContainer()
        self._ping_pong_tasks = asyncio.PriorityQueue()

    async def _make_pings(self):
        """ Task that sends pings to all subscriptions in the queue.
            All subs in this queue have timed out.
        """
        while True:
            await self._check_timeouts()
            while not self._ping_pong_tasks.empty():
                ping_task = await self._ping_pong_tasks.get()
                await ping_task.ping()

            # Go idle so other tasks can run.
            await asyncio.sleep(MAKE_PING_DELAY)

    async def _check_timeouts(self):
        """ Checks all the subscribers to see if their timer has timed out
            and puts all the timed out ones in the priority queue.
        """
        subs = self._sub_container.get_all_subs()
        timed_out_subs = filter(lambda sub: sub.timed_out(), subs)
        for sub in timed_out_subs:
            self._ping_pong_tasks.put_nowait(sub)

    async def _make_publications(self, publication: Publication) -> None:
        """ Sends the publication to all the subscribers of the topic. """
        subs = self._sub_container.get_subs(publication.topic)
        for sub in subs:
            sub.new_data(publication.message)

    async def _add_subscription(self, subscription: Subscription) -> None:
        self._sub_container.add_sub(subscription)

    async def _request_handler(self,
                               reader: asyncio.StreamReader,
                               writer: asyncio.StreamWriter) -> None:
        """ Handles a TCP request. """
        request = Request(reader, writer)
        result = await request.respond()

        if type(result) is Subscription:
            self._sub_container.add_sub(result)

        elif type(result) is Publication:
            self._make_publications(result)

        elif type(result) is None:
            Log.debug('Result is None! ')

    async def start(self) -> None:
        """ Starts the server. This method runs forever. """
        config = Config.get()
        server = await asyncio.start_server(self._request_handler,
                                            config['server']['ip'],
                                            config['server']['port'])
        Log.info(f'Server started at {server.sockets[0].getsockname()}')

        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    Log.init()
    asyncio.run(Server().start())
