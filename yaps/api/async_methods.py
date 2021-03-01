import struct
import asyncio

from yaps.utils import Log
from yaps.api.packet import Packet
from yaps.api import protocol_utils


async def async_read_packet(reader: asyncio.StreamReader) -> Packet:
    try:
        header = await reader.read(protocol_utils.Sizes.HEADER)
        # Log.debug(f'Header: {header}')
        cmd, flags, length = protocol_utils.unpack_header(header)
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
                    protocol_utils.Formats.HEADER)

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
                f'Expected: "{protocol_utils.DEBUG_COMMANDS[cmd]}", '
                f'Got: "{protocol_utils.DEBUG_COMMANDS[packet.cmd]}"')
        if writer is not None:
            await async_send_packet(writer, protocol_utils.Commands.BAD_CMD)
        ok = False

    return ok
