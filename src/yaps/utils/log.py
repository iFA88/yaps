import logging
import os


__all__ = ['Log']


_log = logging.getLogger(__name__)
BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_PATH, 'log')

DEFAULT_DEBUG_LEVEL = logging.DEBUG


class Log:

    _stream = None
    _disabled = False

    def _ensure_log_exists() -> None:
        if not os.path.exists(os.path.dirname(LOG_PATH)):
            os.makedirs(os.path.dirname(LOG_PATH))

    def disable() -> None:
        Log._disabled = True

    def close() -> None:
        if Log._stream is not None:
            Log._stream.close()
            Log._strema = None

    def init(configs: dict = None) -> None:
        try:
            debug_level = configs['debug_level']
        except (KeyError, TypeError):
            debug_level = DEFAULT_DEBUG_LEVEL

        Log._ensure_log_exists()

        # Open stream to file to give to streamhandler.
        Log._stream = open(LOG_PATH, 'w')
        ch = logging.StreamHandler(Log._stream)

        # Set log levels and formats.
        _log.setLevel(debug_level)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s]'
                                      ' - %(message)s',
                                      datefmt='%Y-%M-%d %H:%M:%S')
        ch.setFormatter(formatter)
        _log.addHandler(ch)

    @staticmethod
    def info(msg: str) -> None:
        if not Log._disabled:
            print(msg)
            _log.info(msg)

    @staticmethod
    def err(msg: str) -> None:
        if not Log._disabled:
            _log.error(msg)

    @staticmethod
    def debug(msg: str) -> None:
        if not Log._disabled:
            _log.debug(msg)
