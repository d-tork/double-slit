
import pandas as pd
import random
import uuid
from datetime import datetime

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
    flags = {
        'bankruptcy': ['financial'],
        'unreported_bankruptcy': ['financial', 'integrity'],
        'judgment': ['financial'],
        'cookie_jar': ['integrity'],
        'spillage': ['espionage']
    }

    def __init__(self, n):
        self.n = n
        self._index = 0
        self._hr = self.read_local_hr_file_as_dict()

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self.n:
            self._index += 1
            return self.create_flag()
        raise StopIteration

    @staticmethod
    def read_local_hr_file_as_dict():
        df = pd.read_csv(HRFile.new_names_file, index_col='ueid')
        return df.to_dict(orient='index')

    def create_flag(self):
        emp_ueid = self.get_random_employee_ueid()
        emp_info = self._hr[emp_ueid]
        chosen_flag_reason = random.choice(list(self.flags.keys()))
        flag = Flag(
            name=emp_info['name'],
            emp_type=emp_info['emp_type'],
            ueid=emp_ueid,
            flag=chosen_flag_reason,
            flag_types=self.flags[chosen_flag_reason],
            severity=random.randint(1, 3)
        )
        return flag

    def get_random_employee_ueid(self):
        return random.choice(list(self._hr.keys()))


