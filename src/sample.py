
import pandas as pd
import random
import uuid
from datetime import datetime

import src


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
    names = pd.read_csv(src.NAMES_FILE, squeeze=True)
    emp_types = ['gov', 'ctr', 'other']
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

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self.n:
            self._index += 1
            return self.create_flag()
        raise StopIteration

    def create_flag(self):
        chosen_flag = random.choice(list(self.flags.keys()))
        flag = Flag(
            name=random.choice(self.names),
            emp_type=random.choice(self.emp_types),
            ueid=create_ueid(),
            flag=chosen_flag,
            flag_types=self.flags[chosen_flag],
            severity=random.randint(1, 3)
        )
        return flag


def create_ueid():
    return uuid.uuid4().hex[:9]

