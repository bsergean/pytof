def challengeUrlOpen(url):
    import webbrowser
    webbrowser.open('http://www.pythonchallenge.com/pc/def/' + url + '.html')

def level0():
    '''
    http://www.pythonchallenge.com/pc/def/0.html
    The hint is 2^38
    '''
    a = 2 ** 38
    challengeUrlOpen(str(a))

def createTranslationTable():
    '''
    http://www.pythonchallenge.com/pc/def/map.html
    The hint is:
    K -> M
    O -> E
    E -> G

    It means we have to translate each letter by letter + 2 using
    each letter ascii code
    '''
    import string
    all = string.lowercase
    first = ord(all[0])
    size = len(all)
    newAll = ''
    for s in all:
        code = ord(s)
        letter = chr(code)
        newCode = (code - first + 2) % size        
        newLetter = chr(newCode + first)
        newAll += newLetter
    table = string.maketrans(all, newAll)
    return table

def level1():
    encodedStr = \
''' g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.
'''
    table = createTranslationTable()
    newStr = encodedStr.translate(table)
    print newStr
    challengeUrlOpen('map'.translate(table))

def level2():
    '''
    http://www.pythonchallenge.com/pc/def/ocr.html

    recognize the characters. maybe they are in the book, 
    but MAYBE they are in the page source.

    You have to fetch the html page. Within it you have two comments, 
    the first is:
    find rare characters in the mess below:
    the second is a mess of character. Both are the last comment of the document
    '''
    urlBase = 'http://www.pythonchallenge.com/pc/def/ocr.html'
    import urllib
    fo = urllib.urlopen(urlBase)
    text = fo.read()

    first = text.rfind('<!--')
    last = text.rfind('-->')

    mess = text[first+len('<!--\n'):last-1]
    assert mess[0] == '%'
    assert mess[-1] == '*'

    import string
    url = ''
    for c in mess:
        if c in string.lowercase: url += c

    # rare characters (using the lowercase filter, or using a dict and counting occurences) 
    # form the word 'equality'
    challengeUrlOpen(url)

def level3():
    ''' 
    http://www.pythonchallenge.com/pc/def/equality.html'
    '''
    
level2()
