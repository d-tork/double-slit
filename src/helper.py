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
        self._positions = self.read_positions_file()
        self.create_hr_data()
        self.write_hr_data_to_file()

    def read_original_names(self):
        names = pd.read_csv(self.original_names_file, index_col=None)
        return names

    def read_positions_file(self):
        with open(self.positions_file) as f:
            positions_dict = yaml.load(f, Loader=yaml.FullLoader)
        return self.create_ranked_tuples_from_dict(positions_dict)

    @staticmethod
    def create_ranked_tuples_from_dict(d):
        return tuple((i, kv[0], kv[1]) for i, kv in enumerate(d.items()))

    def create_hr_data(self):
        self.add_ueid()
        self.add_emp_type()

    def add_ueid(self):
        self._new_data['ueid'] = self._new_data['name'].map(self.generate_ueid)

    @staticmethod
    def generate_ueid(s):
        byte_string = s.encode('utf-8')
        full_hash = hashlib.md5(byte_string).hexdigest()
        first_9 = full_hash[:9]
        return first_9

    def add_emp_type(self):
        self._new_data['emp_type'] = random.choices(
            population=self.emp_types,
            weights=[0.3, 0.7],
            k=len(self._names)
        )

    def write_hr_data_to_file(self):
        self._new_data.to_csv(self.new_names_file, index=False)

