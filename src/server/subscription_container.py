from subscription import Subscription
from utils.log import Log


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

    def get_all(self) -> set:
        all_subs = set()
        for subs in self._subscriptions.values():
            all_subs.update(subs)
        return all_subs

    def get(self, topic: str) -> set:
        return self._subscriptions.get(topic, set())

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