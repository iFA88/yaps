import argparse
import asyncio

from yaps.utils import Log, base_parser
from yaps.client import Client


def parse_args() -> argparse.Namespace:
    parser = base_parser()
    parser.add_argument('-t', '--topic', type=str,
                        required=True)
    return parser.parse_args()


def new_data(message):
    print(f'New data received: {message}')


async def main():
    args = parse_args()
    client = Client(args.ip, args.port)

    Log.set_level(args.debug_level)
    await client.subscribe(args.topic, new_data)


if __name__ == '__main__':
    asyncio.run(main())
