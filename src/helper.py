from os import path
import pandas as pd
import hashlib
import random
import yaml

import src


class HRFile(object):
    original_names_file = path.join(src.PROJ_PATH, 'src', 'names.csv')
    new_names_file = path.join(src.PROJ_PATH, 'src', 'hr_names.csv')
    emp_types = ['gov', 'ctr']
    positions_file = path.join(src.PROJ_PATH, 'src', 'positions.yaml')

    def __init__(self):
        self._names = self.read_original_names()
        self._new_data = self._names.copy()
        self._positions = self.read_positions_file_as_tuples()
        self.create_hr_data()
        self.write_hr_data_to_file()

    def read_original_names(self):
        names = pd.read_csv(self.original_names_file, index_col=None)
        return names

    def read_positions_file_as_tuples(self):
        positions_dict = read_yaml_into_dict(self.positions_file)
        return create_ranked_tuples_from_dict(positions_dict)

    def create_hr_data(self):
        self.add_ueid()
        self.add_emp_type()
        self.add_position()

    def add_ueid(self):
        self._new_data['ueid'] = self._new_data['name'].map(generate_ueid)

    def add_emp_type(self):
        self._new_data['emp_type'] = random.choices(
            population=self.emp_types,
            weights=[0.3, 0.7],
            k=len(self._names)
        )

    def add_position(self):
        position_df = pd.DataFrame(self._positions, columns=['rank', 'position', 'team'])
        position_df_resized = position_df.sample(n=len(self._new_data), replace=True)
        position_df_resized.reset_index(drop=True, inplace=True)
        self._new_data = pd.concat([self._new_data, position_df_resized], axis=1)

    def write_hr_data_to_file(self):
        self._new_data.to_csv(self.new_names_file, index=False)


def create_ranked_tuples_from_dict(d):
    return tuple((i, kv[0], kv[1]) for i, kv in enumerate(d.items()))


def generate_ueid(s):
    byte_string = s.encode('utf-8')
    full_hash = hashlib.md5(byte_string).hexdigest()
    first_9 = full_hash[:9]
    return first_9


def read_yaml_into_dict(filepath):
    with open(filepath, 'r') as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)
