import re

from yaps.api.protocol_utils import Commands # noqa
from yaps.api.async_methods import (async_send_packet, async_read_packet,  # noqa
                                    async_cmd_ok)
from yaps.api.sync_methods import send_packet, read_packet, cmd_ok # noqa


DELAY_PING_PONG = 1
PING_PONG_TIMEOUT = 60

# Regex Formats
TOPIC_FORMAT = '[a-zA-Z0-9]+[a-zA-Z0-9/]*'
MESSAGE_FORMAT = '.*'
RE_TOPIC_FORMAT = re.compile(TOPIC_FORMAT)
RE_PUBLISH_FORMAT = re.compile(f'{TOPIC_FORMAT} *\| *{MESSAGE_FORMAT}', # noqa
                               flags=re.DOTALL)

# Used for struct to calcucate correct packet size.
LITTLE_ENDIAN = '>'

# Used for debugging. This list is filled in build_debug_commands() function.
DEBUG_COMMANDS = {}
commands_built = False


def topic_ok(topic: str) -> bool:
    return RE_TOPIC_FORMAT.match(topic)


def publish_ok(data: str) -> bool:
    return RE_PUBLISH_FORMAT.match(data)


def get_topic_and_msg(data: str) -> (str, str):
    """ Returns the topic and the message of the data string. """
    topic, message = data.split('|')
    return topic[:-1], message[1:]
