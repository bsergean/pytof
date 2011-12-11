from __future__ import with_statement
import sys
import pickle
from copy import deepcopy
from pdb import set_trace
from random import randint
import Image, ImageDraw

# alpha shape wrapper
import sys, os
import tempfile
import subprocess

# sys.setrecursionlimit(sys.maxint) # not enought ... :)

def get_alpha_shape(points, hull_path):
    # Write points to tempfile
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    for point in points:
        tmpfile.write("%0.7f %0.7f\n" % point)
    tmpfile.close()

    # Run hull
    command = "%s -A -m1000000 -oN < %s" % (hull_path, tmpfile.name)
    print >> sys.stderr, "Running command: %s" % command
    retcode = subprocess.call(command, shell=True)
    if retcode != 0:
        print >> sys.stderr, "Warning: bad retcode returned by hull.  Retcode value:" % retcode
    os.remove(tmpfile.name)

    # Parse results
    results_file = open("hout-alf")
    results_file.next() # skip header
    results_indices = [[int(i) for i in line.rstrip().split()] for line in results_file]
#    print "results length = %d" % len(results_indices)
    results_file.close()
    os.remove(results_file.name)

    # return [(points[i], points[j]) for i,j in results_indices]
    out = [(points[i], points[j]) for i,j in results_indices]

    flattened_output = []
    # for point_i, point_j in get_alpha_shape(points):
    for point_i, point_j in out:
        # sys.stdout.write("%0.7f,%0.7f\t%0.7f,%0.7f\n" % (point_i[0], point_i[1], point_j[0], point_j[1]))
        flattened_output.append(point_i)
        flattened_output.append(point_j)

    return flattened_output, out

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

    for p in points:
        print p[0], p[1]

    # sys.exit(0)

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
print hull
c.draw_lines(hull, blue)
c.draw_points(points, black)
c.draw_points( [bottom], red )

if True:
    hull_path = '/tmp/hull.exe'
    flattened_lines, lines = get_alpha_shape(sorted_points, hull_path)
    for A, B in lines:
        c.draw_lines([A, B], black)

c.save('out.png')
