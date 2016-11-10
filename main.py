import sys

import dumper
from Elasticsearch_API import ElasticsearchAPI
from config_manager import ConfigManager


__author__ = "Peter Henell"
__copyright__ = "Copyright 2016, Peter Henell"
__credits__ = ["Peter Henell"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Peter Henell"
__email__ = "dnd"
__status__ = "dev"

# polisen_events = 'https://polisen.se/Stockholms_lan/Aktuellt/RSS/Lokal-RSS---Handelser/Lokala-RSS-listor1/Handelser-RSS---Stockholms-lan/?feed=rss'
polisen_news = 'https://polisen.se/Stockholms_lan/Aktuellt/RSS/Lokal-RSS---Nyheter/Lokala-RSS-listor1/Nyheter-RSS---Stockholms-lan/?feed=rss'
polisen_events = 'https://polisen.se/Aktuellt/Handelser/Handelser-i-hela-landet/?feed=rss'


def main(arguments):
    import os.path

    if len(arguments) == 0:
        print('Usage: main.py <settings_file.ini> [truncate_data]')
        print('Specify truncate_data if you wish to clear all the data')
        print()
        print('Example usage: main.py localhost.ini')
        print('Example usage: main.py localhost.ini truncate_data')
        exit(2)

    settings_file = arguments[0]

    if not os.path.isfile(settings_file):
        print('Settings file not found: %s' % settings_file)

    config_manager = ConfigManager.from_file(settings_file)
    es = ElasticsearchAPI.from_config_manager(config_manager)

    # for stat_collector in stat_collectors:
    if len(arguments) == 2:
        if arguments[1] == 'truncate_data':
            es.delete_index('police_events')

    result = dumper.get(polisen_events)
    rssEntries = dumper.parse_to_obj(result)

    es.create_index('police_events')
    mapping = {
            "properties": {
                "published": {
                    "type": "date",
                    "format": "date_hour_minute_second"
                },
                "title": {
                    "type": "string",
                    "index": "analyzed"
                },
                "link": {
                    "type": "string",
                    "index": "analyzed"
                },
                "summary": {
                    "type": "string",
                    "index": "analyzed"
                },
                "location": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "reported_date": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "report_type": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "location_street": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "location_commune": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "location_region": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "html_body": {
                    "type": "string",
                    "index": "analyzed"
                },
            }
        }
    es.set_mapping(index_name='police_events', doc_type='events', mapping=mapping)

    existing_entries = es.find_ids([r['entry_id'] for r in rssEntries], index_name='police_events', doc_type='events')

    new_entries = [e for e in rssEntries if e['entry_id'] not in existing_entries]
    print('Found %i rss items of which %i are new' % (len(rssEntries), len(new_entries)))

    # Getting the HTML body only for the new entries to reduce overhear
    for entry in new_entries:
        entry['html_body'] = dumper.get_link_body(entry['link'])

    es.consume_all(new_entries, index_name='police_events', doc_type='events', id_column_name='entry_id')


if __name__ == '__main__':
    main(sys.argv[1:])
