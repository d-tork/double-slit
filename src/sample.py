
import pandas as pd
import random
from time import sleep
import uuid
import os

from src.example import Flag


class SampleFlagGenerator(object):
    names = pd.read_csv('names.csv', squeeze=True)
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
        print(os.getcwd())

    def generate(self):
        for i in range(self.n):
            sleep(1)
            yield self.create_flag()

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


if __name__ == '__main__':
    a = SampleFlagGenerator(2)
    for i in a.generate():
        print(i)
