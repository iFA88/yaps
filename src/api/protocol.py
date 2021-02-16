import asyncio
import struct

from utils.log import Log
from api.packet import Packet


class Formats:
    CMD = 'B'
    FLAGS = 'B'
    LENGTH = 'I'
    HEADER = f'{CMD}{FLAGS}{LENGTH}'


class Sizes:
    CMD = struct.calcsize(Formats.CMD)
    FLAGS = struct.calcsize(Formats.FLAGS)
    LENGTH = struct.calcsize(Formats.LENGTH)
    HEADER = struct.calcsize(Formats.HEADER)


class Commands:
    PUBLISH = 0
    PUBLISH_ACK = 1
    SUBSCRIBE = 2
    SUBSCRIBE_ACK = 3
    NEW_DATA = 4
    NEW_DATA_ACK = 5
    PING = 6
    PONG = 7
    INCORRECT_FORMAT = 8
    # End of commands


async def read_packet(reader: asyncio.StreamReader) -> Packet:
    header = await reader.read(Sizes.HEADER)
    cmd, flags, length = unpack_header(header)
    data = await reader.read(length)
    return Packet(cmd, flags, length, data)


def unpack_header(header: bytes) -> (int, int, int):
    return struct.unpack(Formats.HEADER, header)


async def send_packet(writer: asyncio.StreamWriter,
                      cmd: int, flags: int, data: bytes = []) -> None:
    length = Sizes.HEADER + len(data)
    packet = Packet(cmd, flags, length, data, Formats.HEADER)

    Log.debug(f'Sending packet: {packet}')

    writer.write(packet.to_bytes())
    await writer.drain()


if __name__ == '__main__':
    Log.init()
    #asyncio.run(tcp_echo_client('Hello World!'))
