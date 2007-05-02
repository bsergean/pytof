def challengeUrlOpen(url):
    import webbrowser
    webbrowser.open('http://www.pythonchallenge.com/pc/def/' + url + '.html')

def level0():
    a = 2 ** 38
    challengeUrlOpen(str(a))

level0()
