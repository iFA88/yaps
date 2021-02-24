import os

# Configurations are stored in ~/.yaps/
# This global is used in by other modules.
BASE_PATH = os.path.expanduser('~/.yaps')

from .log import Log # noqa
from .argparser import base_parser # noqa
from .config import Config # noqa
