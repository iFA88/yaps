import unittest

from ..src.client import Client

IP = '127.0.0.1'
PORT = 9889


class TestSubscribe(unittest.TestCase):

    def setUp(self):
        self.con = Client(IP, PORT)
        self.con.connect()

    def tearDown(self):
        self.con.unsubscribe_all()
        self.con.disconnect()

    def _sub(self, topics: list) -> None:
        for topic in topics:
            for t in [f'{topic}', f'/{topic}', f'{topic}/', f'/{topic}/']:
                self.con.subscribe(t)

    def _unsub(self, topics: list) -> None:
        for topic in topics:
            self.con.unsubscribe(topic)

    def _test_sub(self, topics):
        self._sub(topics)
        self.assertEqual(self.con.get_subscriptions(), topics)

    def _test_unsub(self, topics):
        self._sub(topics)
        self._unsub(topics)
        self.assertEqual(self.con.get_subscriptions(), [])

    def test_sub_to_1_topic(self):
        self._test_sub(['weather'])

    def test_sub_to_2_topic(self):
        self._test_sub(['weather', 'kitchen'])

    def test_sub_to_5_topics(self):
        self._test_sub(['weather', 'kitchen', 'animals', 'farms', 'car'])

    def test_unsub_to_1(self):
        self._test_unsub(['weather'])

    def test_unsub_to_2(self):
        self._test_unsub(['weather', 'kitchen'])

    def test_unsub_to_5(self):
        self._test_unsub(['weather', 'kitchen', 'animals', 'farms', 'car'])
