import unittest
import asyncio
import async_timeout

from client.client import Client
from utils.log import Log
from utils.config import Config


TEST_TIMEOUT = .2


class TestSubscribe(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        Log.init()
        self.ip = Config.get()['client']['ip']
        self.port = Config.get()['client']['port']
        self.client = Client(self.ip, self.port)

    async def test_one_sub(self):
        await self._test_one_sub('test', 'hello world')

    async def test_five_subs(self):
        data = ['asd123', 'cookiemonster', '  stuff -> stuff',
                '{}ªßðªø¡@£ł', '\r\n\\a\\«\\»cSTUFF\rr']
        for msg in data:
            await self._test_one_sub('test', msg)

    async def _test_one_sub(self, topic, expected):
        try:
            with async_timeout.timeout(TEST_TIMEOUT):
                callback = lambda actual: self.assertNewData(expected, actual)   # noqa
                await asyncio.gather(self.client.subscribe(topic, callback),
                                     self.client.publish('test', expected))
        except asyncio.exceptions.TimeoutError:
            pass

    def assertNewData(self, expected: str, actual: str):
        self.assertEqual(expected, actual,
                         f'Expected "{expected}"" but got "{actual}"')

    async def publish(self):
        self.assertTrue(await self.client.publish('test', 'hello world'))


if __name__ == '__main__':
    unittest.main()
