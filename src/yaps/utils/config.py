import json
import os

from yaps.utils.log import Log


__all__ = ['Config']


CONFIG_NAME = 'config.json'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_PATH, CONFIG_NAME)


class Config:

    @staticmethod
    def get() -> dict:
        """ Returns the config file and none if an error occurs. """
        config = {}

        try:
            with open(CONFIG_PATH, 'rb') as f:
                config = json.load(f)
        except FileNotFoundError:
            Log.err(f'Failed to find config at {CONFIG_PATH}')
        except json.decoder.JSONDecodeError as e:
            Log.err(f'Failed to parse JSON {e}')

        return config
