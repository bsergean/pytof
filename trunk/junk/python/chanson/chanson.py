from os.path import exists
from sgmllib import SGMLParser
from sys import exit

def download(url):
    import urllib
    fo = urllib.urlopen(url)
    text = fo.read()
    return text

def get_links(url, song = False):
    fn = url.split('/')[-1] + '.html'
    if exists(fn):
        fo = open(fn, 'r')
        text = fo.read()
    else:
        text = download(url)
        fo = open(fn, 'w')
        fo.write(text)
        fo.close()

    if song:
        return parse_song(text)
    else:
        return parse_listing(text)

class LinkParser(SGMLParser):
    """ blabla """
    def reset(self):
        SGMLParser.reset(self)
        self.links = []

    def start_a(self, attrs):
        link = attrs[0][1]
        if link.startswith('/chanson'):
            self.links.append(link)

def parse_listing(text):
    parser = LinkParser()
    parser.feed(text)
    return parser.links

def unescape(text):
    ''' Handle errors ? '''
    from htmlentitydefs import entitydefs
    head_index, tail_index = 0, 0
    head = '&'
    tail = ';'
    new_text = ''

    while True:
        old = head_index
        head_index = text.find(head, head_index)
        if head_index == -1: break
        tail_index = text.find(tail, head_index)
        if tail_index == -1: break

        #print head_index, tail_index
        accent = text[head_index+1:tail_index]

        new_text += text[old:head_index]
        new_text += entitydefs[accent]

        # We must start after the 'end' from 'endstream'
        head_index = tail_index + 1 
        tail_index = head_index

    if tail_index != 0:
        new_text += text[tail_index:-1]

    return new_text

def clean_text(text):
    text = text[len('small><br>'):-1]
    text = text.replace('<BR>','')

    # FIXME: regexp Does not work ...
    if False:
        import re
        REGEXP = "(?P<text>{.*})"
        regexp = re.compile(REGEXP)
        text = regexp.sub('\g<text>', text)

    return unescape(text).decode('latin1').encode('utf8')

def parse_song(text):
    index = 0
    index = text.find('small', index+1)
    index = text.find('small', index+1)

    index_start = text.find('small', index + 1)
    index_end = text.find('small', index_start + 1)
    lyrics = text[index_start:index_end]
    return clean_text(lyrics)

def sleep():
    import time
    time.sleep(3)

url_base = 'http://www.paroles.net'
tous_suffix = '/artistes/1/tous'

if False:
    #get_links(url_base + tous_suffix)
    #get_links(url_base + '/chansons/1586.1/Zouk-Machine')
    # res = get_links('http://www.paroles.net/chanson/56203.1', True)
    res = get_links('http://www.paroles.net/chanson/28524.1', True)
    print res
    exit(0)

tous = get_links(url_base + tous_suffix)
for a in tous:
    tous_per_artist = get_links(url_base + a)
    print 'Artist %s: %d songs' % (a, len(tous_per_artist))

    for s in tous_per_artist:
        print s
        song = get_links(url_base + s, True)
        print song
        sleep()

