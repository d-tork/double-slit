import unittest
import pandas as pd
import os

from src import hrsource


class HRFileGeneratorClassTestCase(unittest.TestCase):
    def setUp(self):
        self.hr = hrsource.HRFileGenerator()

    def test_original_names_read(self):
        original_names = self.hr.read_original_names()
        self.assertIsInstance(original_names, pd.DataFrame)
        self.assertGreater(len(original_names), 0)

    def test_positions_file_read(self):
        positions = self.hr.read_positions_file()
        self.assertIsInstance(positions, pd.DataFrame)
        self.assertGreater(len(positions), 0)


class HRFileCreationTestCase(unittest.TestCase):
    def setUp(self):
        self.hr = hrsource.HRFileGenerator()
        self.hr_file_test_path = 'test_hr_file.csv'

    def test_add_ueid_col(self):
        self.hr.generate(hr_file_path=self.hr_file_test_path)
        self.assertIn('ueid', self.hr.data)

    def test_add_emptype_col(self):
        self.hr.generate(hr_file_path=self.hr_file_test_path)
        self.assertIn('emp_type', self.hr.data)

    def test_add_position_cols(self):
        self.hr.generate(hr_file_path=self.hr_file_test_path)
        self.assertIn('position', self.hr.data)
        self.assertIn('team', self.hr.data)

    def test_hr_file_created(self):
        self.hr.generate(hr_file_path=self.hr_file_test_path)
        self.assertTrue(os.path.exists(hrsource.HRFile.default_hr_file_path))

    def test_hr_file_has_data(self):
        self.hr.generate(hr_file_path=self.hr_file_test_path)
        hr_test = pd.read_csv(self.hr_file_test_path)
        self.assertTrue(len(hr_test) > 0)
        self.assertIn('ueid', hr_test)
        self.assertIn('emp_type', hr_test)
        self.assertIn('position', hr_test)

    def tearDown(self):
        os.remove(self.hr_file_test_path)


class HRFileTestCase(unittest.TestCase):
    sample_existing_path = 'test_sample_df.csv'
    sample_not_existing_path = 'test_not_a_sample_df.csv'

    def setUp(self):
        self.create_sample_file()

    def create_sample_file(self):
        df = pd.DataFrame([1, 2, 3, 4], columns="ABCD".split())
        df.to_csv(self.sample_existing_path, index=False)

    def test_read_local_hr_file_when_exists(self):
        sample = hrsource.read_local_hr_file(self.sample_existing_path)
        self.assertIsInstance(sample, pd.DataFrame)
        self.assertTrue(len(sample) > 0)

    def test_read_local_raises_no_file_found(self):
        self.assertRaises(
            FileNotFoundError,
            hrsource.read_local_hr_file,
            hr_file_path=self.sample_not_existing_path)

    def test_creates_file_when_not_exist(self):
        hr = hrsource.HRFile(hr_file_path=self.sample_not_existing_path)
        self.assertTrue(os.path.exists(self.sample_not_existing_path))

    def tearDown(self):
        os.remove(self.sample_existing_path)
        if os.path.exists(self.sample_not_existing_path):
            os.remove(self.sample_not_existing_path)


class HelperFunctionsTestCase(unittest.TestCase):
    def test_generate_ueid(self):
        s = 'John Smith'
        string_hash = hrsource.generate_ueid(s)
        self.assertEqual(string_hash, '6117323d2')


if __name__ == '__main__':
    unittest.main()
