
from os import listdir
from os.path import exists

class MyDict(dict):

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

from UserDict import UserDict

class odict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)

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
