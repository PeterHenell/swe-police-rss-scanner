import feedparser
import datetime
from PolisenHTMLParser import PolisenHTMLParser


sample = """{
    "guidislink": false,
    "id": "http://polisen.se/Stockholms_lan/Aktuellt/Handelser/Stockholms-lan/2015-06-05-1510-Trafikolycka-personskada-Stockholm/_Fri,-05-Jun-2015-13:49:03-GMT",
    "link": "http://polisen.se/Stockholms_lan/Aktuellt/Handelser/Stockholms-lan/2015-06-05-1510-Trafikolycka-personskada-Stockholm/",
    "links": [
        {
            "href": "http://polisen.se/Stockholms_lan/Aktuellt/Handelser/Stockholms-lan/2015-06-05-1510-Trafikolycka-personskada-Stockholm/",
            "rel": "alternate",
            "type": "text/html"
        }
    ],
    "published": "Fri, 05 Jun 2015 13:49:03 GMT",
    "published_parsed": [
        2015,
        6,
        5,
        13,
        49,
        3,
        4,
        156,
        0
    ],
    "summary": "Hammarbybacken, Johanneshov. Bilist och motorcyklist har krockat.",
    "summary_detail": {
        "base": "",
        "language": null,
        "type": "text/html",
        "value": "Hammarbybacken, Johanneshov. Bilist och motorcyklist har krockat."
    },
    "title": "2015-06-05 15:10, Trafikolycka, personskada, Stockholm",
    "title_detail": {
        "base": "",
        "language": null,
        "type": "text/plain",
        "value": "2015-06-05 15:10, Trafikolycka, personskada, Stockholm"
    }
}"""


def get(url):
    d = feedparser.parse(url)
    return d
    # u'Sample Feed'


def get_html(url):
    import urllib3
    import urllib3, certifi
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', url)
    return r.data.decode('utf-8')


def parse_html(html_string):
    p = PolisenHTMLParser()
    p.reset()
    p.feed(html_string)
    p.close()
    return p.data


def parse_datetime(str_arr):
    # d = datetime.datetime(str_arr[0], str_arr[1], str_arr[2], str_arr[3], str_arr[4], str_arr[5], str_arr[6])
    d = datetime.datetime(str_arr[0], str_arr[1], str_arr[2], str_arr[3], str_arr[4], str_arr[5])
    return d


def get_link_body(link):
    html_string = get_html(link)
    # parsed = parse_html(html_string)
    # print('%s %s' % (link, parsed))
    return html_string


def parse_location(title):
    if len(title.split(',')) > 2:
        arr = title.split(',')
        # The last entry should be the location
        return arr[len(arr)-1]
        # return title.split(',')[2]
    return title


def parse_reported_date(title):
    return title.split(',')[0]


def parse_report_type(title):
    return title.split(',')[1]


def parse_street(summary):
    if len(summary.split('.')) > 1:
        return summary.split('.')[0]
    return summary


def parse_commune(summary):
    if len(summary.split('.')) > 1:
        return summary.split('.')[1]
    return summary


def parse_to_obj(json_string):
    l = []
    for entry in json_string['entries']:
        x = {
            "entry_id": entry['id'],
            "summary": entry['summary'],
            "title": entry['title'],
            "link": entry['link'],
            "published": parse_datetime(entry['published_parsed']),

            "publication": {
                "year": parse_datetime(entry['published_parsed']).year,
                "month": parse_datetime(entry['published_parsed']).month,
                "day_of_month": parse_datetime(entry['published_parsed']).day,
                "hour": parse_datetime(entry['published_parsed']).hour,
                "minute": parse_datetime(entry['published_parsed']).minute,
            },
            "location": parse_location(entry['title']),
            "reported_date": parse_reported_date(entry['title']),
            "report_type": parse_report_type(entry['title']),
            "location_street": parse_street(entry['summary']),
            "location_commune": parse_commune(entry['summary']),
        }

        l.append(x)
    return l


def print_json(json_string):
    import json
    print(json.dumps(json_string, sort_keys=True,
                     indent=4, separators=(',', ': ')))