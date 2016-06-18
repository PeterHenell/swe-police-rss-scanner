import urllib3

from html.parser import HTMLParser


class PolisenHTMLParser(HTMLParser):

    recording = 0
    data = []

    def error(self, message):
        pass

    # def __init__(self, convert_charrefs=True):
    #     self.__init__(convert_charrefs)
    #     self.recording = 0
    #     self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'id' and value == 'column2-3':
                    # print(name, value)
                    # print("Encountered the beginning of a %s tag" % tag)
                    self.recording += 1

    def handle_endtag(self, tag):
        if tag == 'div':
            self.recording -= 1
            # print("Encountered the end of a %s tag" % tag)

    def handle_data(self, data):
        if self.recording:
            # print(data)
            text = data.strip()
            if len(text) > 0:
                text = text.replace('[ \t\r\n]+', ' ')
                self.data.append(text)



 # p = MyHTMLParser()
 # f = urllib2.urlopen('http://www.someurl.com')
 # html = f.read()
 # p.feed(html)
 # print p.data
 # p.close()