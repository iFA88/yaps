import argparse
import asyncio
import sys

from client.publish import Publish


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
    pub = Publish(topic, message, ip=ip, port=port)
    await pub.start()


if __name__ == '__main__':

    args = parse_args()
    asyncio.run(publish(args.topic, args.message, args.ip, args.port))
