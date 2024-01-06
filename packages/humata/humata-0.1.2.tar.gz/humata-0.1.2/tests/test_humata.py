import unittest

import humata


class TestSimple(unittest.TestCase):

    def test_add(self):
        self.assertEqual((humata.Number(5) + humata.Number(6)).value, 11)


if __name__ == '__main__':
    unittest.main()
