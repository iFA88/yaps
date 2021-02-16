import asyncio

from api import protocol
from server_request import Request
from utils.config import Config
from utils.log import Log


async def request_handler(reader: asyncio.StreamReader,
                          writer: asyncio.StreamWriter) -> None:
    req = Request(reader, writer)
    await req.respond()
    #packet = await protocol.read_packet(reader)



async def main() -> None:
    config = Config.get()
    server = await asyncio.start_server(request_handler,
                                        config['server']['ip'],
                                        config['server']['port'])
    Log.info(f'Server started at {server.sockets[0].getsockname()}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    Log.init()
    asyncio.run(main())
