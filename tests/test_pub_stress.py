import unittest

from yaps.client import AsyncClient
from yaps.utils.config import Config
from yaps.utils.log import Log


class TestStress(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.ip = Config.get()['client']['ip']
        self.port = Config.get()['client']['port']
        self.client = AsyncClient(self.ip, self.port)
        Log.disable()

    async def test_topics_formats(self):
        ROUNDS = 100
        for i in range(ROUNDS):
            await self.client.publish('test', f'Msg: {i}')


if __name__ == '__main__':
    unittest.main()
