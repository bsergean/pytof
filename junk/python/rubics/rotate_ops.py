#! /usr/bin/env python
# coding: utf-8

# XXX Rename to xform or something (not starting with a r)

from colors import *
from cube_ops import *

def rubicC(f1, f2, f3):
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = f3
    f3 = [
        c7,
        c4,
        c1,
        c8,
        c5,
        c2,
        c9,
        c6,
        c3
    ]
    f3 = [cubeC(*cube) for cube in f3]

    return f1, f2, f3

def rubicCC(f1, f2, f3):
    ''' Could implement that with 3 rubicC '''
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = f3
    f3 = [
        c3,
        c6,
        c9,
        c2,
        c5,
        c8,
        c1,
        c4,
        c7
    ]
    f3 = [cubeCC(*cube) for cube in f3]

    return f1, f2, f3

def rubicF2C(f1, f2, f3):
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = f2
    f2 = [
        c7,
        c4,
        c1,
        c8,
        c5,
        c2,
        c9,
        c6,
        c3
    ]
    f2 = [cubeC(*cube) for cube in f2]

    return f1, f2, f3

def rubicF1C(f1, f2, f3):
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = f1
    f1 = [
        c7,
        c4,
        c1,
        c8,
        c5,
        c2,
        c9,
        c6,
        c3
    ]
    f1 = [cubeC(*cube) for cube in f1]

    return f1, f2, f3

def rubicTR(f1, f2, f3):
    ''' T for top, R for right
    '''
    c11, c12, c13, c14, c15, c16, c17, c18, c19 = f1
    c21, c22, c23, c24, c25, c26, c27, c28, c29 = f2
    c31, c32, c33, c34, c35, c36, c37, c38, c39 = f3

    f1 = [
        cubeR(*c13),
        cubeR(*c23),
        cubeR(*c33),

        c14, # 4 to 9 are invariant
        c15,
        c16,
        c17,
        c18,
        c19
    ]

    f2 = [
        cubeR(*c12),
        cubeR(*c22),
        cubeR(*c32),

        c24, # 4 to 9 are invariant
        c25,
        c26,
        c27,
        c28,
        c29
    ]

    f3 = [
        cubeR(*c11),
        cubeR(*c21),
        cubeR(*c31),

        c34, # 4 to 9 are invariant
        c35,
        c36,
        c37,
        c38,
        c39
    ]
    return f1, f2, f3

def rubicTL(f1, f2, f3):
    ''' T for top, L for left 
    '''
    f1, f2, f3 = rubicTR( f1, f2, f3 )
    f1, f2, f3 = rubicTR( f1, f2, f3 )
    return rubicTR( f1, f2, f3 )

def rubicMR(f1, f2, f3):
    c11, c12, c13, c14, c15, c16, c17, c18, c19 = f1
    c21, c22, c23, c24, c25, c26, c27, c28, c29 = f2
    c31, c32, c33, c34, c35, c36, c37, c38, c39 = f3

    f1 = [
        c11, # first three invariants
        c12,
        c13,

        cubeR(*c16),
        cubeR(*c26),
        cubeR(*c36),

        c17, # last three invariants
        c18,
        c19
    ]

    f2 = [
        c21, # first three invariants
        c22,
        c23,

        cubeR(*c15),
        cubeR(*c25),
        cubeR(*c35),

        c27, # last three invariants
        c28,
        c29
    ]

    f3 = [
        c31, # first three invariants
        c32,
        c33, 

        cubeR(*c14),
        cubeR(*c24),
        cubeR(*c34),

        c37, # last three invariants
        c38,
        c39
    ]
    return f1, f2, f3

def rubicML(f1, f2, f3):
    ''' T for top, L for left 
    '''
    f1, f2, f3 = rubicMR( f1, f2, f3 )
    f1, f2, f3 = rubicMR( f1, f2, f3 )
    return rubicMR( f1, f2, f3 )
    
def rubicBR(f1, f2, f3):
    c11, c12, c13, c14, c15, c16, c17, c18, c19 = f1
    c21, c22, c23, c24, c25, c26, c27, c28, c29 = f2
    c31, c32, c33, c34, c35, c36, c37, c38, c39 = f3

    f1 = [
        c11, # 1 to 6 invariants
        c12,
        c13,
        c14,
        c15,
        c16,
        cubeR(*c19),
        cubeR(*c29),
        cubeR(*c39),
    ]

    f2 = [
        c21, # 1 to 6 invariants
        c22,
        c23,
        c24,
        c25,
        c26,
        cubeR(*c18),
        cubeR(*c28),
        cubeR(*c38),
    ]

    f3 = [
        c31, # 1 to 6 invariants
        c32,
        c33,
        c34,
        c35,
        c36,
        cubeR(*c17),
        cubeR(*c27),
        cubeR(*c37),
    ]

    return f1, f2, f3

def rubicBL(f1, f2, f3):
    ''' B for bottom, L for left 
    '''
    f1, f2, f3 = rubicBR( f1, f2, f3 )
    f1, f2, f3 = rubicBR( f1, f2, f3 )
    return rubicBR( f1, f2, f3 )

def rubicUpsideDown(f1, f2, f3):
    f1, f2, f3 = rubicC(f1, f2, f3)
    f1, f2, f3 = rubicC(f1, f2, f3)

    f1, f2, f3 = rubicF2C(f1, f2, f3)
    f1, f2, f3 = rubicF2C(f1, f2, f3)

    f1, f2, f3 = rubicF1C(f1, f2, f3)
    f1, f2, f3 = rubicF1C(f1, f2, f3)

    return f1, f2, f3

def rubicRight(f1, f2, f3):
    f1, f2, f3 = rubicTR(f1, f2, f3)
    f1, f2, f3 = rubicMR(f1, f2, f3)
    f1, f2, f3 = rubicBR(f1, f2, f3)

    return f1, f2, f3

def rubicLeft(f1, f2, f3):
    f1, f2, f3 = rubicTL(f1, f2, f3)
    f1, f2, f3 = rubicML(f1, f2, f3)
    f1, f2, f3 = rubicBL(f1, f2, f3)

    return f1, f2, f3

if __name__ == '__main__':
    # Back to front: f1, f2, f3
    f1 = [
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange],
        [green, blue, white, yellow, red, orange]
    ]
    f2 = [
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange]
    ]
    f3 = [
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange],
        [green, red, white, yellow, red, orange]
    ]

    f1, f2, f3 = rubicC(f1, f2, f3)
