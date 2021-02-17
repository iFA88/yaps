import asyncio

from api import protocol
from utils.log import Log


SLEEP_SLOT_TIME = 1         # In seconds.


class State:
    PING_PONG = 1
    PING_PONG_1_MISS = 2
    PING_PONG_2_MISS = 2


class Subscription:

    def __init__(self,
                 topic: str,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        self._time = 0
        self._state = State.PING_PONG
        self._reader = reader
        self._writer = writer
        self._alive = True

        self._set_identifier(topic)

    async def start_idle(self) -> None:
        """ Sets the task into idle sleep, count up a timer.
            When the timer reaches timeout, timed_out() will return True.
        """
        while self._alive:
            # Go idle so other tasks can run.
            await asyncio.sleep(SLEEP_SLOT_TIME)

            # Update timer.
            self._time += SLEEP_SLOT_TIME

        self.die()

    def _next_state(self) -> bool:
        """ Advances to the next state. Returns true if the subscription
            should be kept alive, and false if it should die.
        """
        alive = True
        if self._state == State.PING_PONG:
            self._state = State.PING_PONG_1_MISS
        elif self._state == State.PING_PONG_1_MISS:
            self._state = State.PING_PONG_2_MISS
        elif self._state == State.PING_PONG_2_MISS:
            alive = False

        return alive

    async def ping(self) -> None:
        """ Pings the subscriber and waits for a PONG back.
            If the subscriber doesn't pong back, the subscription is closed.
        """
        await protocol.send_packet(self._writer, protocol.Commands.PING)
        Log.debug(f'[{self.topic, self.fd}] Ping')

        pong = await protocol.read_packet(self._reader)
        if not await protocol.cmd_ok(pong, protocol.Commands.PONG):
            alive = self._next_state()
            if not alive:
                self._alive = False

    async def new_data(self, topic: str, message: str) -> None:
        # Send new data to subscriber
        await protocol.send_packet(self._writer, protocol.Commands.NEW_DATA)

        # Wait for SUBSCRIBE_ACK
        response = await protocol.read_packet(self._reader)

        # If no ACK is recieved, close the connection.
        if not await protocol.cmd_ok(response, protocol.Commands.NEW_DATA_ACK,
                                     self._writer):
            self.close()

        # Reset timer.
        self._time = 0

    def timed_out(self):
        self._time > protocol.DELAY_PING_PONG

    def close(self):
        Log.debug(f'Closing connection: {self}')
        self._alive = False

    def die(self):
        Log.debug(f'Subscription died {self}')

    def _set_identifier(self, topic: str) -> None:
        """ Sets the identification of the subscription.
            This consists of:
            1. Topic
            2. File descripter number from reader/writer stream.
        """
        self.topic = topic,
        self.fd = self._writer.get_extra_info('socket').fileno()

    def __repr__(self):
        return self.topic, self.fd

    def __lt__(self, other):
        return self._time - other._time
