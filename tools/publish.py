import argparse
import asyncio

from yaps.utils import Log, base_parser
from yaps.client import AsyncClient


def parse_args() -> argparse.Namespace:
    parser = base_parser()
    parser.add_argument('-t', '--topic', type=str,
                        required=True)
    parser.add_argument('-m', '--message', type=str,
                        required=True)
    return parser.parse_args()


async def main():
    args = parse_args()
    client = AsyncClient(args.ip, args.port)

    Log.set_level(args.debug_level)
    await client.publish(args.topic, args.message)


if __name__ == '__main__':
    asyncio.run(main())
