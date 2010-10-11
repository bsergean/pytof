#!/usr/bin/env python

def my_dec(f):

    def new_f(*args, **kwargs):
        print f.func_name, args, kwargs
        f(*args, **kwargs)

    return new_f

@my_dec
def foo(a, b):
    ''' Does foo
    '''
    return a ** 2

def run():
    foo(4, 5)
    foo(5, 6)

def bar(L):
    import copy
    # K = copy.deepcopy(L)
    K = copy.deepcopy(L)
    K.append(['caca'])
    K[0].append('nan')
    print K

if __name__ == '__main__':
    run()    

    L = [['foo', 'bar'],['toto', 'tata']]
    bar(L)
    print L


