import unittest
import threading

from yaps.client import Client
from yaps.utils.config import Config
from yaps.utils.log import Log


TEST_TIMEOUT = 0.2


class TestSubscribe(unittest.TestCase):

    def setUp(self):
        self.ip = Config.get()['client']['ip']
        self.port = Config.get()['client']['port']
        self.client = Client(self.ip, self.port)
        Log.disable()

    @unittest.skip(True)
    def test_one_sub(self):
        self._test_one_sub('test', 'hello world')
        self._test_one_sub('test2', 'hello world2')
        self._test_one_sub('test3', 'hello world3')

    @unittest.skip(True)
    def test_five_subs(self):
        data = ['asd123', 'cookiemonster', '    stuff -> stuff',
                '{}ªßðªø¡@£ł', '¡@£]]€¡}£€~', '  space much  space  ']
        for msg in data:
            self._test_one_sub('test', msg)

    def _test_one_sub(self, topic, expected):
        callback = lambda actual: self.assertNewData(expected, actual)   # noqa
        sub = threading.Thread(target=self.client.subscribe,
                               args=(topic, callback), daemon=True)
        sub.start()
        self.client.publish('test', expected)

    def assertNewData(self, expected: str, actual: str):
        self.assertEqual(expected, actual,
                         f'Expected "{expected}"" but got "{actual}"')

    def publish(self):
        self.assertTrue(self.client.publish('test', 'hello world'))


if __name__ == '__main__':
    unittest.main()
