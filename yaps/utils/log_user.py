from yaps.utils import Log


class BasicLogUser:

    def set_loglevel(self, level: str) -> None:
        """ Log level can be one either an int from the classic logging module
            or any string of:
            - 'notset'
            - 'debug'
            - 'info'
            - 'warning'
            - 'error'
            - 'critical'
        """
        Log.set_level(level)

    def disable_log():
        Log.disable()
