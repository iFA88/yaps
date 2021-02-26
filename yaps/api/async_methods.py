import struct
import asyncio

from yaps.utils import Log
from .packet import Packet
from . import protocol


async def async_read_packet(reader: asyncio.StreamReader) -> Packet:
    try:
        header = await reader.read(protocol.Sizes.HEADER)
        # Log.debug(f'Header: {header}')
        cmd, flags, length = protocol.unpack_header(header)
        # Log.debug(f'CMD: {cmd} Flags: {flags} Lengt: {length}')
        data = await reader.read(length)
        return Packet(cmd, flags, length, data)
    except struct.error as e:
        Log.debug(f'Failed to read packet: {e}')
        return None
    except RuntimeError:
        Log.debug('Race condition reading packet.')


async def async_send_packet(writer: asyncio.StreamWriter,
                            cmd: int, flags: int = 0,
                            data: bytes = b'') -> None:
    packet = Packet(cmd, flags, len(data), data,
                    protocol.Formats.HEADER)

    # Log.debug(f'Sending packet: {packet}')

    writer.write(packet.to_bytes())
    await writer.drain()


async def async_cmd_ok(packet: Packet, cmd: int,
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
                f'Expected: "{protocol.DEBUG_COMMANDS[cmd]}", '
                f'Got: "{protocol.DEBUG_COMMANDS[packet.cmd]}"')
        if writer is not None:
            await async_send_packet(writer, protocol.Commands.BAD_CMD)
        ok = False

    return ok
