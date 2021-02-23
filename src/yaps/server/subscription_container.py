try:
    from subscription import Subscription
except ModuleNotFoundError:
    from yaps.server.subscription import Subscription
from yaps.utils.log import Log


TOPIC_WILDCARD = '*'


class SubscriptionContainer:
    """
        Helper class for storing the subscriptions in the server.
        This is a very primitive solution where the subscriptions are stored
        in a dictionary like:
        {
            'topic': {Subscription1, Subscription2},
            'topic2': {Subscription3, Subscription4}
        }
        where the values are sets of subscriptions.
        This class is used by the server and should not be used directly.
    """

    def __init__(self):
        self._subscriptions = {}
        self._wildcards = {}

    def get_all(self) -> set:
        all_subs = set()
        for subs in self._subscriptions.values():
            all_subs.update(subs)
        return all_subs

    def get(self, sub_topic: str) -> list:
        """ Returns all subscriptions subscribed to the given topic. """
        # Using helper method to get all subs because wildcards make it
        # slightly harder than just getting them from dictionary.
        subscriptions = []
        for topic, subs in self._subscriptions.items():
            if self._topic_match(sub_topic, topic):
                subscriptions.extend(subs)
        return subscriptions

    def _topic_match(self, topic: str, pattern: str) -> bool:
        """ Checks wether "pattern" matches the "topic".
            This is a helper method to decide if a subscriber
            is subscribing to a certain topic, since wildcards
            can be used.
        """

        # Ensure that the depths of the topics match.
        real_topic = topic.split('/')
        pattern_topic = pattern.split('/')
        if len(real_topic) != len(pattern_topic):
            return False

        # Check that every part of the topic matches and ignore if wildcard.
        for real_part, part in zip(real_topic, pattern_topic):
            if part == TOPIC_WILDCARD:
                continue
            elif part != real_part:
                return False

        return True

    def add(self, subscription: Subscription) -> None:
        topic = subscription.topic

        # Create a new set if topic is new.
        if topic not in self._subscriptions:
            self._subscriptions[topic] = set()

        self._subscriptions[topic].add(subscription)

    def delete(self, subscription: Subscription) -> bool:
        topic = subscription.topic
        del_ok = False
        try:
            self._subscriptions[topic].remove(subscription)
            subscription.die()
            del_ok = True

            # Remove topic if there's no subscribers left.
            if len(self._subscriptions[topic]) == 0:
                self._subscriptions[topic].remove(topic)

        except KeyError:
            Log.debug(f'Failed to find sub on topic {topic}')

        return del_ok
