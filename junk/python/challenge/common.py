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

def level1():
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
        print newLetter
        newAll += newLetter
    table = string.maketrans(all, newAll)
    encodedStr = \
''' g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.
'''
    newStr = encodedStr.translate(table)
    print newStr
    challengeUrlOpen('map'.translate(table))

def level2():
    '''
    http://www.pythonchallenge.com/pc/def/ocr.html

    recognize the characters. maybe they are in the book, 
    but MAYBE they are in the page source.
    '''

level1()
