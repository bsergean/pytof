#! /usr/bin/env python
# coding: utf-8

from colors import *

# XXX: add arrows
# Up and Down have the same invariants (Right and Left)
def cubeU(Front, Back, Top, Bottom, Right, Left):
    return [
        Bottom,
        Top,
        Front,
        Back,
        Right,
        Left
    ]

def cubeD(Front, Back, Top, Bottom, Right, Left):
    return [
        Top,
        Bottom,
        Back,
        Front,
        Right,
        Left
    ]

# Right (Clock wise) and Left (Counter clock wise) 
# have the same invariants (Front and Back)
def cubeC(Front, Back, Top, Bottom, Right, Left):
    return [
        Front,
        Back,
        Left,
        Right,
        Top,
        Bottom 
    ]

def cubeCC(Front, Back, Top, Bottom, Right, Left):
    return [
        Front,
        Back,
        Right,
        Left,
        Bottom,
        Top
    ]

# Right and Left have the same invariants (Top and Bottom)
def cubeR(Front, Back, Top, Bottom, Right, Left):
    return [
        Left,
        Right,
        Top,
        Bottom,
        Front,
        Back 
    ]

def cubeL(Front, Back, Top, Bottom, Right, Left):
    return [
        Right,
        Left,
        Top,
        Bottom,
        Back,
        Front
    ]

if __name__ == '__main__':
    assert cubeU(green, blue, white, yellow, red, orange) == \
             [yellow, white, green, blue, red, orange]

    assert cubeD(green, blue, white, yellow, red, orange) == \
             [white, yellow, blue, green, red, orange]

    assert cubeC(green, blue, white, yellow, red, orange) == \
             [green, blue, orange, red, white, yellow]

    assert cubeCC(green, blue, white, yellow, red, orange) == \
             [green, blue, red, orange, yellow, white]

    assert cubeR(green, blue, white, yellow, red, orange) == \
             [orange, red, white, yellow, green, blue]

    assert cubeL(green, blue, white, yellow, red, orange) == \
            [red, orange, white, yellow, blue, green]

    template = '''
    return [
        X,
        X,
        X,
        X,
        X,
        X
    ]
    '''
