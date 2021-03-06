#!/Users/dtork/PycharmProjects/double-slit/venv/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import random
from os import path

import src
from src.hrsource import read_yaml_into_dict
from src.sample import SampleFlagGenerator


def main():
    es_config_path = path.join(src.PROJ_PATH, 'src', 'elastic_config.yaml')
    es_config = read_yaml_into_dict(es_config_path)
    es = Elasticsearch(hosts=[es_config])

    random.seed()
    iterations = random.randint(1, 50)
    try:
        for sample_flag in SampleFlagGenerator(iterations):
            sample_flag.push_to_es(es)
    except ConnectionError:
        raise RuntimeError('Connection to Elasticsearch cluster failed')


if __name__ == '__main__':
    main()
