from decimal import Decimal, getcontext
from re import findall

def find_recurring_part(a, found):
    '''
    >>> re.findall(r'(\d+)\1', '32323232')
    ['3232']
    '''
    result = findall(r'(\d+)\1', a)
    print a, result, found
    if len(result) == 0:
        return a if found else None
    else:
        return find_recurring_part(result[0], True)

def recurring_cycle(i):
    q = Decimal(1) / Decimal(i)
    q = str(q)[2:]
    return find_recurring_part(q, False)

getcontext().prec = 1000
assert ( recurring_cycle(2) == None)
assert ( recurring_cycle(3) == '3')
