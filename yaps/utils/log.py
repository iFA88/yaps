import logging
import os
import sys

from . import BASE_PATH

__all__ = ['Log']


_log = logging.getLogger()
LOG_PATH_SERVER = os.path.join(BASE_PATH, 'server.log')
LOG_PATH_CLIENT = os.path.join(BASE_PATH, 'client.log')

# Used to convert cli params
DEBUG_LEVELS = {
    'notset': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}
DEFAULT_DEBUG_LEVEL = logging.DEBUG


class Log:

    _stream = None

    @staticmethod
    def _ensure_logdir_exists() -> None:
        if not os.path.exists(os.path.dirname(LOG_PATH_SERVER)):
            os.makedirs(os.path.dirname(LOG_PATH_SERVER))

    @staticmethod
    def disable() -> None:
        logging.getLogger('asyncio').disabled = True
        _log.disabled = True

    @staticmethod
    def close() -> None:
        if Log._stream is not None:
            Log._stream.close()
            Log._strema = None

    @staticmethod
    def init(server: bool = True, debug_level: str = None) -> None:
        debug_level = DEBUG_LEVELS.get(debug_level, DEFAULT_DEBUG_LEVEL)

        Log._ensure_logdir_exists()

        # Open stream to file to give to streamhandler.
        log_path = LOG_PATH_SERVER if server else LOG_PATH_CLIENT
        Log._stream = open(log_path, 'a')
        ch = logging.StreamHandler(Log._stream)

        # Set log levels and formats.
        _log.setLevel(debug_level)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s]'
                                      ' - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        # Add stdout stream
        stdin_handler = logging.StreamHandler(sys.stdout)

        stdin_handler.setFormatter(formatter)
        ch.setFormatter(formatter)

        _log.addHandler(stdin_handler)
        _log.addHandler(ch)

    @staticmethod
    def set_level(debug_level: str = None) -> None:
        if type(debug_level) is str:
            debug_level = DEBUG_LEVELS.get(debug_level, DEFAULT_DEBUG_LEVEL)
        _log.setLevel(debug_level)

    @staticmethod
    def info(msg: str) -> None:
        _log.info(msg)

    @staticmethod
    def warning(msg: str) -> None:
        _log.warning(msg)

    @staticmethod
    def critical(msg: str) -> None:
        _log.critical(msg)

    @staticmethod
    def err(msg: str) -> None:
        _log.error(msg)

    @staticmethod
    def debug(msg: str) -> None:
        _log.debug(msg)
