
from os import listdir
from os.path import exists

class MyDict(dict):
    '''

    Missing methods:

    __iter__
    >>> a = {}
    >>> a['foo'] = 1
    >>> a['bar'] = 2
    >>> it = a.__iter__()
    >>> it.next()
    'foo'
    >>> it.next()
    'bar'

    '''

    def __init__(self):
        self._items = list()

    def __contains__(self, key):
        """To implement lowercase keys."""
        for k,v in self._items:
            if k == key:
                return True
        return False

    def __delitem__(self, key):
        for i, (k,v) in enumerate(self._items):
            if k == key:
                self._items.pop(i)
                return

        raise KeyError(item)

    def __getitem__(self, key):
        """To implement lowercase keys."""
        for k,v in self._items:
            if k == key:
                return v
            
        raise KeyError(item)
    
    def __setitem__(self, key, item):
        if key not in [k for k,v in self._items]: 
            self._items.append( (key, item) )

    def __len__(self):
        return len(self._items)

    def clear(self):
        self._items = []
    
    def items(self):
        return self._items
    
    def keys(self):
        return [k for k, _ in self._items]

    def values(self):
        return [v for _, v in self._items]

if __name__ == '__main__':
    
    d = MyDict()
    d['tintin'] = 'milou'
    d['batman'] = 'robin'

    print len(d)
    print d['tintin']
    # print d['haddock']

    del d['tintin']
    print len(d)

    print 'batman' in d
    print 'zorro' in d

    print d.items()
    print d.keys()
    print d.keys()
