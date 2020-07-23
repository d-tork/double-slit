
from elasticsearch import Elasticsearch

from src.sample import SampleFlagGenerator


def main():
    es = Elasticsearch(hosts=[
        {'host': 'synapse', 'port': '9200'}
    ])

    for sample_flag in SampleFlagGenerator(10):
        sample_flag.push_to_es(es)


if __name__ == '__main__':
    main()
