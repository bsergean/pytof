
from copy import deepcopy
def multiply_each_slow(input):
    '''
    There is an array A[N] of N integers. 
    You have to compose an array Output[N] such that Output[i] will 
    be equal to the product of all the elements of A[] except A[i].

    Example:
            INPUT:[4, 3, 2, 1, 2]
            OUTPUT:[12, 16, 24, 48, 24]

    Note: Solve it without the division operator and in O(n).
    '''
    output = deepcopy(input)
    for i, dummy in enumerate(input):
        tmp = deepcopy(input)
        tmp[i] = 1
        output[i] = reduce(lambda x,y: x*y, tmp)

    return output

def multiply_each_log(input):
    '''
    There is an array A[N] of N integers. 
    You have to compose an array Output[N] such that Output[i] will 
    be equal to the product of all the elements of A[] except A[i].

    Example:
            INPUT:[4, 3, 2, 1, 2]
            OUTPUT:[12, 16, 24, 48, 24]

    Note: Solve it without the division operator and in O(n).
    '''
    from math import log, exp
    L = sum(log(i) for i in input)

    output = [L - log(i) for i in input]
    output = map(exp, output)
    output = map(round, output)

    return output

in_ = [4, 3, 2, 1, 2]
out = [12, 16, 24, 48, 24]
assert (out == multiply_each_slow(in_))
assert (out == multiply_each_log(in_))

