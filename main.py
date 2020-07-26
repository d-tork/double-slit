#!/Users/dtork/PycharmProjects/double-slit/venv/bin/python3
from elasticsearch import Elasticsearch
from src.sample import SampleFlagGenerator
import random
from os import path

import src


def main():
    es_config_path = path.join(src.PROJ_PATH, 'src', 'elastic_config.yaml')
    es_config = src.helper.read_yaml_into_dict(es_config_path)
    es = Elasticsearch(hosts=[es_config])

    random.seed()
    iterations = random.randint(10, 500)
    for sample_flag in SampleFlagGenerator(iterations):
        sample_flag.push_to_es(es)


if __name__ == '__main__':
    main()
