from os.path import exists
from sgmllib import SGMLParser

def download(url):
    import urllib
    fo = urllib.urlopen(url)
    text = fo.read()
    return text

def tous():
    tous_fn = 'tous.txt'
    if exists(tous_fn):
        fo = open(tous_fn, 'r')
        text = fo.read()
    else:
        tous_url = 'http://www.paroles.net/artistes/1/tous'
        text = download(tous_url)
        fo = open(tous_fn, 'w')
        fo.write(text)
        fo.close()

    parse_tous(text)

class LinkParser(SGMLParser):
    """ blabla """
    def reset(self):
        SGMLParser.reset(self)
        self.entries = {}

    def start_a(self, attrs):
        link = attrs[0][1]
        if link.startswith('/chansons'):
            print link

def parse_tous(text):
	parser = LinkParser()
	parser.feed(text)

tous()
