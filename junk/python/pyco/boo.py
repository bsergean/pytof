
def foo():
    return 'foo'

def bar():
    return 'bar'

def baz(param = None):
    if param == 'quiet': 
        return 'quiet'
    if param == 'baba': 
        return 'baba'
    if param is None: 
        return 'baz'

    if param == 'baba': return 'baba'
    if param is None: return 'baz'
    if param == None: return 'baz'

'''
The number one reason you're gonna turn this option off is if you have to compile a large piece of code. I forgot the limit but above several megs (for your binary) the linker fails when thumbs is turned on.
'''
