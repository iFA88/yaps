import unittest

from yaps.utils.log import Log
from yaps.server.subscription_container import SubscriptionContainer
from yaps.server.subscription import Subscription


class TestPublish(unittest.TestCase):

    def setUp(self):
        self.container = SubscriptionContainer()
        Log.disable()

    def test_normal_topics(self):
        for topic in ['test', 'test/test', 'test/test/test']:
            self.container.add(Subscription(topic, None, None))

        self.assertEqual(len(self.container.get('test')), 1)

    def test_wildcards(self):
        for topic in ['test', 'test/*', 'test/*/*',
                      'test/*/test']:
            self.container.add(Subscription(topic, None, None))

        self.assertEqual(len(self.container.get('test')), 1)
        self.assertEqual(len(self.container.get('test/test')), 1)
        self.assertEqual(len(self.container.get('test/test/test')), 2)

    def test_basic(self):
        self.container.add(Subscription('hey', None, None))
        self.assertEqual(len(self.container.get('hey')), 1)


if __name__ == '__main__':
    unittest.main()
