import unittest
from src.sample import SampleFlagGenerator, FlagTypes


class SampleFlagGeneratorTestCase(unittest.TestCase):
    def test_generates_correct_number_of_samples(self):
        five_flags = [flag for flag in SampleFlagGenerator(5)]
        self.assertEqual(len(five_flags), 5)

    def test_generates_dict(self):
        flag = SampleFlagGenerator(1)
        self.assertIsInstance(next(flag), dict)


class FlagsTypesTestCase(unittest.TestCase):
    def setUp(self):
        self.flag_types = FlagTypes()

    def test_flagtypes_is_dict(self):
        self.assertIsInstance(self.flag_types, dict)

    def test_flagtypes_not_empty(self):
        # TODO: choose correct assert with IDE help
        self.assertTrue(len(self.flag_types) > 0)


if __name__ == '__main__':
    unittest.main()
