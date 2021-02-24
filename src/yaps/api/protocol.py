import asyncio
import re
import struct

from yaps.utils.log import Log
from yaps.api.packet import Packet


__all__ = ['Commands', 'read_packet', 'send_packet', 'DELAY_PING_PONG',
           'PING_PONG_TIMEOUT', 'topic_ok', 'publish_ok']


DELAY_PING_PONG = 1
PING_PONG_TIMEOUT = 2

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


async def read_packet(reader: asyncio.StreamReader) -> Packet:
    try:
        header = await reader.read(Sizes.HEADER)
        # Log.debug(f'Header: {header}')
        cmd, flags, length = unpack_header(header)
        # Log.debug(f'CMD: {cmd} Flags: {flags} Lengt: {length}')
        data = await reader.read(length)
        return Packet(cmd, flags, length, data)
    except struct.error as e:
        Log.debug(f'Failed to read packet: {e}')
        return None
    except RuntimeError:
        Log.debug('Race condition reading packet.')


def unpack_header(header: bytes) -> (int, int, int):
    return struct.unpack(Formats.HEADER, header)


async def send_packet(writer: asyncio.StreamWriter,
                      cmd: int, flags: int = 0, data: bytes = b'') -> None:
    packet = Packet(cmd, flags, len(data), data, Formats.HEADER)

    # Log.debug(f'Sending packet: {packet}')

    writer.write(packet.to_bytes())
    await writer.drain()


def get_command(self, cmd: int) -> str:
    return str(cmd)


async def cmd_ok(packet: Packet,
                 cmd: int,
                 writer: asyncio.StreamWriter = None) -> bool:
    """
        Returns true if command is okay, and logs if not.
        If the command is INCORRECT, a packet is sent to the
        client with BAD_CMD command.
    """
    ok = True
    if packet is None:
        Log.debug('Failed to read packet!')
        ok = False
    elif packet.cmd != cmd:
        Log.err('Packet command incorrect! '
                f'Expected: "{DEBUG_COMMANDS[cmd]}", '
                f'Got: "{DEBUG_COMMANDS[packet.cmd]}"')
        if writer is not None:
            await send_packet(writer, Commands.BAD_CMD)
        ok = False

    return ok


def topic_ok(topic: str) -> bool:
    return RE_TOPIC_FORMAT.match(topic)


def publish_ok(data: str) -> bool:
    return RE_PUBLISH_FORMAT.match(data)


def get_topic_and_msg(data: str) -> (str, str):
    return [part for part in data.split('|')]
