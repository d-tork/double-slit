#!/Users/dtork/PycharmProjects/double-slit/venv/bin/python3
from elasticsearch import Elasticsearch
from src.sample import SampleFlagGenerator
import random


def main():
    es = Elasticsearch(hosts=[
        {'host': 'synapse', 'port': '9200'}
    ])

    random.seed()
    iterations = random.randint(10, 500)
    for sample_flag in SampleFlagGenerator(iterations):
        sample_flag.push_to_es(es)


if __name__ == '__main__':
    main()
