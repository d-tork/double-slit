from os import path
import pandas as pd
import hashlib

import src


def create_ueid_for_names():
    original_names_file = path.join(src.PROJ_PATH, 'src', 'names.csv')
    new_names_file = path.join(src.PROJ_PATH, 'src', 'names_with_id.csv')
    names = pd.read_csv(original_names_file, index_col=None)
    names['ueid'] = names['name'].map(generate_hash)
    names.to_csv(new_names_file, index=False)


def generate_hash(s):
    byte_string = s.encode('utf-8')
    full_hash = hashlib.md5(byte_string).hexdigest()
    first_9 = full_hash[:9]
    return first_9
