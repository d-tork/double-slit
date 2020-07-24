import unittest
import pandas as pd
import os

from src import helper


class HRFileCreationTestCase(unittest.TestCase):
    def test_original_names_read(self):
        hr = helper.HRFile()
        self.assertIsInstance(hr._names, pd.DataFrame)
        self.assertGreater(len(hr._names), 0)

    def test_hr_file_created(self):
        hr = helper.HRFile()
        self.assertTrue(os.path.exists(hr.new_names_file))

    def test_generate_ueid(self):
        s = 'John Smith'
        hash = helper.HRFile.generate_ueid(s)
        self.assertEqual(hash, '6117323d2')

    def test_add_ueid_col(self):
        hr = helper.HRFile()
        self.assertIn('ueid', hr._new_data)

    def test_add_emptype_col(self):
        hr = helper.HRFile()
        self.assertIn('emp_type', hr._new_data)

    def test_add_position_cols(self):
        hr = helper.HRFile()
        self.assertIn('position', hr._new_data)
        self.assertIn('team', hr._new_data)


class PositionsYAMLTestCase(unittest.TestCase):
    def setUp(self):
        self.d = {'Quarterback': 'Offense', 'Left Tackle': 'Defense'}

    def test_positions_from_yaml_are_tuple(self):
        t = helper.HRFile.create_ranked_tuples_from_dict(self.d)
        self.assertIsInstance(t, tuple)
        self.assertIsInstance(t[0], tuple)

    def test_positions_are_ranked(self):
        t = helper.HRFile.create_ranked_tuples_from_dict(self.d)
        qb_is_rank_0 = t[0]
        self.assertEqual(qb_is_rank_0, (0, 'Quarterback', 'Offense'))


if __name__ == '__main__':
    unittest.main()
