from os import path
import pandas as pd
import hashlib
import random
import yaml

import src


class HRFile(object):
    default_hr_file_path = path.join(src.PROJ_PATH, 'src', 'hr_names.csv')

    def __init__(self, *args, **kwargs):
        self.data = None
        self.data = self.get_hr_data(*args, **kwargs)

    @staticmethod
    def get_hr_data(*args, **kwargs):
        while True:
            try:
                data = read_local_hr_file(*args, **kwargs)
                break
            except FileNotFoundError:
                hrgen = HRFileGenerator()
                hrgen.generate(*args, **kwargs)
        return data


class HRFileGenerator(object):
    names_file = path.join(src.PROJ_PATH, 'src', 'names.csv')
    positions_file = path.join(src.PROJ_PATH, 'src', 'positions.yaml')
    _emp_types = ['gov', 'ctr']

    def __init__(self):
        self.data = pd.DataFrame()

    def generate(self, *args, **kwargs):
        original_names = self.read_original_names()
        self.data = original_names.copy()
        self.create_hr_data()
        self.write_hr_data_to_file(*args, **kwargs)

    def read_original_names(self):
        names = pd.read_csv(self.names_file, index_col=None)
        return names

    def read_positions_file(self):
        positions_dict = read_yaml_into_dict(self.positions_file)
        positions = pd.DataFrame.from_dict(positions_dict, orient='index')
        positions = positions.reset_index().reset_index()
        positions.columns = ['rank', 'position', 'team']
        return positions

    def create_hr_data(self):
        self.add_ueid()
        self.add_emp_type()
        self.add_position()

    def add_ueid(self):
        self.data['ueid'] = self.data['name'].map(generate_ueid)

    def add_emp_type(self):
        self.data['emp_type'] = random.choices(
            population=self._emp_types,
            weights=[0.3, 0.7],
            k=len(self.data)
        )

    def add_position(self):
        positions_df = self.read_positions_file()
        positions_df_resized = positions_df.sample(n=len(self.data), replace=True)
        positions_df_resized.reset_index(drop=True, inplace=True)
        self.data = pd.concat([self.data, positions_df_resized], axis=1)

    def write_hr_data_to_file(self, hr_file_path=HRFile.default_hr_file_path):
        self.data.to_csv(hr_file_path, index=False)


def read_local_hr_file(hr_file_path=HRFile.default_hr_file_path):
    print(hr_file_path)
    return pd.read_csv(hr_file_path, index_col=None)


def generate_ueid(s):
    byte_string = s.encode('utf-8')
    full_hash = hashlib.md5(byte_string).hexdigest()
    first_9 = full_hash[:9]
    return first_9


def read_yaml_into_dict(filepath):
    with open(filepath, 'r') as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)


if __name__ == '__main__':
    a = HRFile('test.csv')
    print(a.data)