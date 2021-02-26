import asyncio

from yaps.api import protocol
from yaps.utils.log import Log


SLEEP_SLOT_TIME = 1         # In seconds.


class State:
    PING_PONG = 1
    PING_PONG_1_MISS = 2
    PING_PONG_2_MISS = 3


class Subscription:
    """
        Abstraction for handling a subscription.
        This class has utilites that lets it increment a counter and indicate
        if it has timed out or not.
        It can also send new data to the subscriber.
    """

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
        Log.debug(f'Ping {self}')

        pong = await protocol.read_packet(self._reader)
        if await protocol.async_cmd_ok(pong, protocol.Commands.PONG):
            # If PONG, reset timer.
            self._time = 0
        else:
            Log.err(f'Bad ping! {self._alive} -> {self._state}')
            # If no PONG, advance to next state, and potentially close.
            alive = self._next_state()
            if not alive:
                self.die()

    async def new_data(self, message: str) -> bool:
        """ Sends the new data to the subscriber.
            Returns true if succesful, false if not.
        """
        send_ok = True
        try:
            # Send new data to subscriber
            await protocol.send_packet(self._writer,
                                       protocol.Commands.NEW_DATA,
                                       data=message.encode('utf-8'))

            # Wait for SUBSCRIBE_ACK
            response = await protocol.read_packet(self._reader)
        except (BrokenPipeError, ConnectionResetError):
            send_ok = False

        if send_ok:
            # If no ACK is recieved, close the connection.
            if not await protocol.async_cmd_ok(response,
                                               protocol.Commands.NEW_DATA_ACK,
                                               self._writer):
                send_ok = False

        if not send_ok:
            self.die()

        # Reset timer.
        self._time = 0
        return send_ok

    def timed_out(self):
        return self._time > protocol.PING_PONG_TIMEOUT

    def is_dead(self) -> bool:
        return not self._alive

    def die(self) -> None:
        if not self._alive:
            return
        self._alive = False
        Log.debug(f'Subscription died {self}')

    def _set_identifier(self, topic: str) -> None:
        """ Sets the identification of the subscription.
            This consists of:
            1. Topic
            2. File descripter number from reader/writer stream.
        """
        self.topic = topic
        try:
            self.fd = self._writer.get_extra_info('socket').fileno()
        except AttributeError:
            # Streams are incorrect
            Log.err(f'Incorrect streams to subscription to {self.topic}')
            self.fd = None

    def __repr__(self):
        return f'| ID:{self.fd} Topic: {self.topic} |'

    def __lt__(self, other):
        return self._time - other._time
