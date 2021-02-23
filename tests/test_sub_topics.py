import unittest

from utils.log import Log
from server.subscription_container import SubscriptionContainer
from server.subscription import Subscription


class TestPublish(unittest.TestCase):

    def setUp(self):
        self.container = SubscriptionContainer()

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


if __name__ == '__main__':
    Log.disable()
    unittest.main()
