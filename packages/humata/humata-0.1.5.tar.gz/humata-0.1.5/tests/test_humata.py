import unittest
import humata


class TestSimple(unittest.TestCase):
    def test_version(self):
        self.assertTrue(isinstance(humata.__version__, str))


if __name__ == "__main__":
    unittest.main()
