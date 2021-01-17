import unittest
from watermarker import LSBWatermarker


class TestWatermarker(unittest.TestCase):

    def test_get_binary_message(self):
        message = "secret"
        binary_message = "011100110110010101100011011100100110010101110100"
        self.assertEqual(LSBWatermarker.get_binary_message(message), binary_message)


if __name__ == "__main__":
    unittest.main()
