import unittest
from src.sample import SampleFlagGenerator


class SampleFlagGeneratorTestCase(unittest.TestCase):
    def test_generates_correct_number_of_samples(self):
        five_flags = [flag for flag in SampleFlagGenerator(5)]
        self.assertEqual(len(five_flags), 5)

    def test_generates_dict(self):
        flag = SampleFlagGenerator(1)
        self.assertIsInstance(next(flag), dict)


if __name__ == '__main__':
    unittest.main()
