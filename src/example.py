
from datetime import datetime
from elasticsearch import Elasticsearch


class Flag(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['flag_datetime'] = datetime.now()

    def push_to_es(self, es_instance):
        es_instance.index(
            index='my-index',
            doc_type='flag',
            body=self
        )


def main():
    es = Elasticsearch(hosts=[
        {'host': 'synapse', 'port': '9200'}
    ])

    sample_flag = Flag(
        name='John Smith',
        emp_type='ctr',
        ueid='12c34d56f',
        flag_types=['financial'],
        flag='unreported_bankruptcy',
        severity=2
    )
    sample_flag.push_to_es(es)


if __name__ == '__main__':
    main()
