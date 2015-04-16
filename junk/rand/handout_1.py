import random

def test1():
    A = random.sample(range(10000), 100)
    A.sort()
    print A

    def search(n, L):
        if L == []:
            return False

        m = len(L) / 2
        print m, L

        if n == L[m]:
            return True
        if len(L) == 1:
            return False

        if n > L[m]:
            return search(n, L[m:])
        else:
            return search(n, L[:m])

    print search(5000, A)
    x = A[12]
    print search(x, A)

def test2():
    class NotANumber(Exception): pass
    def atoi(s):
        # return int(s)
        table = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
        }

        s = s[::-1]
        res = 0
        for i,e in enumerate(s):
            if e not in table:
                raise NotANumber
            res += table[e] * 10 ** i

        return res

    assert atoi('12341234213399') == 12341234213399
    
test2()
