import json
import os

from yaps.utils.log import Log


__all__ = ['Config']


CONFIG_NAME = 'config.json'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_PATH, CONFIG_NAME)


class Config:

    __default = {
        'client': {
            'ip': '127.0.0.1',
            'port': 8999
        },
        'server': {
            'ip': '127.0.0.1',
            'port': 8999
        }
    }

    _config = None

    @staticmethod
    def get() -> dict:
        """
            Returns the configurations.
            If can't find the configuration file, default parameters are used.
        """

        # Only need to read the config once (assumes no live-changes).
        if Config._config is None:
            try:
                with open(CONFIG_PATH, 'rb') as f:
                    Config._config = json.load(f)
            except FileNotFoundError:
                Log.err(f'Failed to find config at {CONFIG_PATH}')
                Config._config = Config.__default
            except json.decoder.JSONDecodeError as e:
                Log.err(f'Failed to parse JSON {e}')
                Config._config = Config.__default

        return Config._config
