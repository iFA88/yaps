import struct

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
