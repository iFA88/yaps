import argparse
import asyncio

from client.client import Client


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--topic', type=str,
                        required=True)
    parser.add_argument('-i', '--ip', type=str,
                        required=False, default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int,
                        required=False, default=8989)
    return parser.parse_args()


async def subscribe(topic: str, ip: str, port: int):
    client = Client(ip, port)
    await client.subscribe(topic, lambda msg: print(msg))


if __name__ == '__main__':

    args = parse_args()
    asyncio.run(subscribe(args.topic, args.ip, args.port))
