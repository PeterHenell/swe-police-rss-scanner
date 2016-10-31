import logging

from elasticsearch import Elasticsearch
from elasticsearch import helpers


logger = logging.getLogger('perf-collector')
handler = logging.StreamHandler()
logger.addHandler(handler)


class ElasticsearchAPI:
    """
    Each query will have its own index based on query name.
    index_name = query.name
    Doc type = query_name to make it possible to set mapping. Mapping is set per doc_type.

    All rows from a Query should look the same no matter the source.

    This makes all the data from all the servers in the same index.
        Comparable.
        Less indexes.
    """
    def __init__(self, host, port, user, password):
        logger.info("Connecting to ES %s..." % host)
        self.es = Elasticsearch(hosts=[
            {'host': host, 'port': port}, ])
        logger.debug(self.es.info())

    @staticmethod
    def from_config_manager(config_manager):
        config = config_manager.get_config('Elasticsearch')

        return ElasticsearchAPI(config['host'],
                                config['port'],
                                config['password'],
                                config['username'])

    def consume_all(self, items, doc_type, index_name):
        print('Pushing %s docs to index: %s' % (len(items), index_name))
        actions = []
        for doc in items:
            action = {
                "_index": index_name,
                "_type": doc_type,
                "_source": doc,
                }
            actions.append(action)
        helpers.bulk(self.es, actions)
        self.es.indices.refresh()

        return len(items)

    def init_indexes_for(self, sources):
        for source in sources:
            self.init_index_for_source(source)

    def set_mapping(self, index_name, doc_type, source_mapping):
        self.es.indices.put_mapping(
            index=index_name,
            doc_type=doc_type,
            body=source_mapping)

    def delete_index(self, index_name):
        print('Truncating data in index: %s' % index_name)
        self.es.indices.delete(index=index_name, ignore=404)

    def create_index(self, index_name):
        print('Creating index %s' % index_name)
        self.es.indices.create(index_name, ignore=400)
