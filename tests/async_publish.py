import unittest

from yaps.client import AsyncClient
from yaps.utils.config import Config
from yaps.utils.log import Log


class TestPublish(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.ip = Config.get()['client']['ip']
        self.port = Config.get()['client']['port']
        self.client = AsyncClient(self.ip, self.port)
        Log.disable()

    async def test_topics_formats(self):
        # Test different topic formats, which should pass.
        topics = ['Test', 'Test', 'Test/Test', 'Test/Test/Test',
                  '0789', '0789/', '0789/0789', '0789/0789/0789']
        for topic in topics:
            self.assertTrue(await self.client.publish(topic, 'TestTopic'))

        # Test different topic formats, which should NOT pass.
        topics = ['/', '//', '///', '.', ',', '_', '-', '|', '$', '@', '\'']
        for topic in topics:
            self.assertFalse(await self.client.publish(topic, 'Test'))

    async def test_message_formats(self):
        # Test different topic formats
        msgs = ['Test', 'Test with white space',
                'Test with random chars: ¡@£€$£¥€[$}}«©·̣',
                'Test with line break: \r\n -> \r\n',
                'Test with json data: {"cookie": ["butter", "chocolate"]}']
        for msg in msgs:
            self.assertTrue(await self.client.publish('TestMsg', msg))


if __name__ == '__main__':
    unittest.main()
