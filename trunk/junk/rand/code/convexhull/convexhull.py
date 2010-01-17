from __future__ import with_statement
import sys
import pickle
from copy import deepcopy
from pdb import set_trace
from random import randint
import Image, ImageDraw

sys.setrecursionlimit(sys.maxint) # not enought ... :)

class Canvas():
    def __init__(self, W, H):
        self.photo = Image.new('RGB', (W, H), white)
        self.draw = ImageDraw.Draw(self.photo)

    def draw_points(self, points, color = None):
        if color is None:
            color = green

        for p in points:
            self.draw.point( p, color )

    def draw_lines(self, points, color = None):
        if color is None:
            color = blue

        self.draw.line( points, color, 5 )
        self.draw.line( [points[-1], points[0]], color, 5 )

    def save(self, output):
        self.photo.save(output, "PNG")

def ccw(p1, p2, p3):
    # return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)
    ret = (p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1])*(p3[0] - p1[0])
    print '\t', ret, p1, p2, p3 
    return ret

def deserialize(input):
    fd = open(input)
    lines = fd.read().splitlines()
    points = []

    W = len(lines[0])
    H = len(lines)

    for i, line in enumerate(lines):
        for j, elem in enumerate(line):
            if elem == '+':
                # the +1 to match position when editing input.txt with
                # ruler on in vim
                points.append( ( j, i) ) 

    fd.close()
    return W, H, points

###
#  Start here
###
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

if False:
    input = sys.argv[1]
    W, H, points = deserialize(input)
else:
    k = 1000
    W, H = k, k
    points = [ (randint(1, k), randint(1, k)) for _ in xrange(k/10) ]

c = Canvas(W, H)

M = ( 
        sum( P[0] for P in points) / len(points),
        sum( P[1] for P in points) / len(points)
    )
bottom = max(points, key=lambda x: x[1])
i = points.index(bottom)
tmp = points[0]
points[0] = points[i]
points[i] = tmp

sorted_points = sorted(points, cmp = lambda N,P: ccw(bottom, N, P))
assert bottom == sorted_points[0]

c.draw_lines( sorted_points, green )

def convex_hull(points):
    hull = points[0:2]
    for i in xrange(2, len(points)):
        print i
        while len(hull) > 1 \
                and ccw(hull[-2], hull[-1], points[i]) > 0:
            # Should be < 0
            print '\tpop'
            hull.pop()
        hull.append(points[i])
        print '\tappend', len(hull)

    print len(hull)
    return hull

for p in sorted_points:
    print p

hull = convex_hull(sorted_points)
c.draw_lines(hull, blue)
c.draw_points(points, black)
c.draw_points( [bottom], red )

c.save('out.png')
