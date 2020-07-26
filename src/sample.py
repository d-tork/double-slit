import pandas as pd
import random
from datetime import datetime
from os import path
import yaml

import src
from src.helper import HRFile


class Flag(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['flag_datetime'] = datetime.now()

    def push_to_es(self, es_instance):
        response = es_instance.index(
            index='my-index',
            doc_type='flag',
            body=self
        )
        print(response)


class SampleFlagGenerator(object):
    """adapted from https://www.programiz.com/python-programming/iterator"""

    def __init__(self, n):
        self.n = n
        self._index = 0
        self._hr = self.read_local_hr_file_as_dict()
        self._flag_types = FlagTypes()

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self.n:
            self._index += 1
            return self.create_flag()
        raise StopIteration

    @staticmethod
    def read_local_hr_file_as_dict():
        df = pd.read_csv(HRFile.default_hr_file_path, index_col='ueid')
        return df.to_dict(orient='index')

    def create_flag(self):
        emp_ueid = self.get_random_employee_ueid()
        emp_info = self._hr[emp_ueid]
        chosen_flag_type = self.get_random_flag_type()
        flag = Flag(
            ueid=emp_ueid,
            name=emp_info['name'],
            flag=chosen_flag_type,
            flag_types=self._flag_types[chosen_flag_type],
            severity=random.randint(1, 3),
            emp_type=emp_info['emp_type'],
            position=emp_info['position'],
            team=emp_info['team']
        )
        return flag

    def get_random_employee_ueid(self):
        return random.choice(list(self._hr.keys()))

    def get_random_flag_type(self):
        return random.choice(list(self._flag_types.keys()))


class FlagTypes(dict):
    flags_file = path.join(src.PROJ_PATH, 'src', 'flags.yaml')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(self.read_flags_file_as_dict())

    def read_flags_file_as_dict(self):
        flags = src.helper.read_yaml_into_dict(self.flags_file)
        return flags


