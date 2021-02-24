import argparse

from .config import Config


def base_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str,
                        required=False, default=Config.get()['server']['ip'])
    parser.add_argument('-p', '--port', type=int,
                        required=False, default=Config.get()['server']['port'])
    parser.add_argument('-d', '--debug_level', type=str,
                        required=False, default='info')
    return parser
