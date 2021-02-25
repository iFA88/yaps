import argparse
import asyncio

from yaps.utils import Log, base_parser
from yaps.server import Server


def parse_args() -> argparse.Namespace:
    parser = base_parser()
    return parser.parse_args()


async def main():
    args = parse_args()
    server = Server(args.ip, args.port)

    Log.set_level(args.debug_level)
    await server.start()


if __name__ == '__main__':
    asyncio.run(main())
