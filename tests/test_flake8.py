import os
import unittest
import subprocess

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_CODE = os.path.join(BASE_PATH, 'src')


class TestFlake8(unittest.TestCase):

    def test_flake8(self):
        pipe = subprocess.run(['flake8', SOURCE_CODE], stdout=subprocess.PIPE)
        result = pipe.stdout.decode('utf-8')
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
