import json
import os

from yaps.utils.log import Log
from . import BASE_PATH

__all__ = ['Config']


CONFIG_PATH = os.path.join(BASE_PATH, 'config.json')


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
            If can't find the configuration file, default parameters are used
            and a new one is created on disk.
        """
        success = False

        # Only need to read the config once (assumes no live-changes).
        if Config._config is None:
            try:
                with open(CONFIG_PATH, 'rb') as f:
                    Config._config = json.load(f)
                    success = True
            except FileNotFoundError:
                Log.err(f'Failed to find config at {CONFIG_PATH}')
            except json.decoder.JSONDecodeError as e:
                Log.err(f'Failed to parse JSON {e}')

            if not success:
                Config._config = Config.__default
                Config._save_config(Config._config)

        return Config._config

    @staticmethod
    def _save_config(config: dict) -> None:
        Log.info(f'Saving configuration file at {CONFIG_PATH}')
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f)
