import argparse
import asyncio

from client.client import Client


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--topic', type=str,
                        required=True)
    parser.add_argument('-m', '--message', type=str,
                        required=True)
    parser.add_argument('-i', '--ip', type=str,
                        required=False, default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int,
                        required=False, default=8989)
    return parser.parse_args()


async def publish(topic: str, message: str, ip: str, port: int):
    client = Client(ip, port)
    await client.publish(topic, message)


if __name__ == '__main__':

    args = parse_args()
    asyncio.run(publish(args.topic, args.message, args.ip, args.port))