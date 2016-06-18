import dumper

polisen_events = 'https://polisen.se/Stockholms_lan/Aktuellt/RSS/Lokal-RSS---Handelser/Lokala-RSS-listor1/Handelser-RSS---Stockholms-lan/?feed=rss'
polisen_news = 'https://polisen.se/Stockholms_lan/Aktuellt/RSS/Lokal-RSS---Nyheter/Lokala-RSS-listor1/Nyheter-RSS---Stockholms-lan/?feed=rss'
polisen_events_sample = r'E:\Source\github\rss-dumper\sample\events.xml'


result = dumper.get(polisen_events_sample)
rssEntries = dumper.parse_to_obj(result)

for entry in rssEntries:
    dumper.print_json(entry)
