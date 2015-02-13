#!/usr/bin/env python
from pdb import set_trace

def run(N, K):
    # power = [True, False]
    # state = ['OFF', 'OFF']

    power = 1
    state = 0

    def snap():
        '''
        [True, False] ['OFF', 'OFF']
        
        snap -> [True, True] ['ON', 'OFF']

        I snap my fingers again, which toggles both Snappers 
        and then promptly cuts power off from the second one, 
        leaving it in the ON state,
        snap -> [True, False] ['OFF', 'ON']
        '''

        for i in xrange(L):
            if state[i] and power[i] and i+1 < L:
                power[i+1] = True

        for i in xrange(L):
            if not state[i] and i+1 < L:
                power[i+1] = False

        for i in xrange(L):
            if not power[i]:
                j = i
                while j < L:
                    power[j] = False
                    j += 1
                break
            
        # print power

    while K > 0:
        snap()
        K -= 1
        print K

    return 'ON' if power == state == 1<<N else 'OFF'

if __name__ == '__main__':
    assert run(2, 3) == 'ON'
    assert run(1, 0) == 'OFF'
    assert run(1, 1) == 'ON'
    assert run(4, 0) == 'OFF'
    assert run(4, 47) == 'ON'

    import sys
    # sys.exit(0)

    lines = open('in.txt').read().splitlines()
    lines.pop(0)
    i = 1
    for line in lines:
        N, K = map(int, line.split())

        sys.stderr.write('%d\n' % i)
        print 'Case #%d: %s' % (i, run(N, K))
        i += 1
