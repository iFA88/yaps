import re
import struct

from .async_methods import async_send_packet, async_read_packet, async_cmd_ok
from .sync_methods import send_packet, read_packet, cmd_ok


__all__ = ['Commands', 'DELAY_PING_PONG', 'PING_PONG_TIMEOUT', 'topic_ok',
           'publish_ok', 'async_send_packet', 'async_read_packet',
           'async_cmd_ok', 'send_packet', 'read_packet', 'cmd_ok']


DELAY_PING_PONG = 1
PING_PONG_TIMEOUT = 60

# Regex Formats
TOPIC_FORMAT = '[a-zA-Z0-9]+[a-zA-Z0-9/]*'
MESSAGE_FORMAT = '.*'
RE_TOPIC_FORMAT = re.compile(TOPIC_FORMAT)
RE_PUBLISH_FORMAT = re.compile(f'{TOPIC_FORMAT} *\| *{MESSAGE_FORMAT}', # noqa
                               flags=re.DOTALL)

# Used for struct to calcucate correct packet size.
LITTLE_ENDIAN = '>'

# Used for debugging. This list is filled in build_debug_commands() function.
DEBUG_COMMANDS = {}
commands_built = False


class Formats:
    CMD = 'B'
    FLAGS = 'B'
    LENGTH = 'I'
    HEADER = f'{LITTLE_ENDIAN}{CMD}{FLAGS}{LENGTH}'


class Sizes:
    CMD = struct.calcsize(f'={Formats.CMD}')
    FLAGS = struct.calcsize(f'={Formats.FLAGS}')
    LENGTH = struct.calcsize(f'{LITTLE_ENDIAN}{Formats.LENGTH}')
    HEADER = struct.calcsize(Formats.HEADER)


class Commands:
    PUBLISH = 0
    PUBLISH_ACK = 1
    PUBLISH_OK = 10
    SUBSCRIBE = 2
    SUBSCRIBE_ACK = 3
    SUBSCRIBE_OK = 11
    NEW_DATA = 4
    NEW_DATA_ACK = 5
    PING = 6
    PONG = 7
    INCORRECT_FORMAT = 8
    BAD_CMD = 9
    # End of commands


def build_debug_commands():
    global DEBUG_COMMANDS
    commands = list(filter(lambda attr: not attr.startswith('_'),
                           dir(Commands)))
    values = [getattr(Commands, cmd) for cmd in commands]
    DEBUG_COMMANDS = {value: cmd for value, cmd in zip(values, commands)}


# Build debug commands
build_debug_commands()


def unpack_header(header: bytes) -> (int, int, int):
    return struct.unpack(Formats.HEADER, header)


def topic_ok(topic: str) -> bool:
    return RE_TOPIC_FORMAT.match(topic)


def publish_ok(data: str) -> bool:
    return RE_PUBLISH_FORMAT.match(data)


def get_topic_and_msg(data: str) -> (str, str):
    """ Returns the topic and the message of the data string. """
    topic, message = data.split('|')
    return topic[:-1], message[1:]
