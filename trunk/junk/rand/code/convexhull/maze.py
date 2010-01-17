from __future__ import with_statement
import sys
import pickle
from copy import deepcopy
from pdb import set_trace

sys.setrecursionlimit(sys.maxint) # not enought ... :)

def serialize():
    # >>> image.getcolors()
    # [(7210300, (255, 255, 255)), (1050, (0, 255, 0)), (550, (255, 0, 0)), (350, (128
    # , 0, 0)), (750, (0, 128, 0)), (4263125, (0, 0, 0))]

    import Image
    image = Image.open('maze.png')

    colors = {
        (255, 255, 255): 'W', 
        (0, 255, 0): 'G', 
        (255, 0, 0): 'R', 
        (128 , 0, 0): 'X', 
        (0, 128, 0): 'Y', 
        (0, 0, 0): 'B',
    }

    W, H = image.size
    new_image = []
    # We serialize line by line
    for j in xrange(0, H, 5):
        line = []
        for i in xrange(0, W, 5):
            pixel = image.getpixel( (i,j) )
            color = colors[pixel] 
            line.append( color )

        new_image.append( ''.join(line) )

    fd = open('maze.txt', 'w')
    fd.write( '%d %d\n' % (W / 5, H / 5) )
    fd.write( '\n'.join( new_image ) )
    fd.close()

# serialize()
# sys.exit(0)

def deserialize(input):
    fd = open(input)
    image = []

    lines = fd.read().splitlines()

    for line in lines[1:]:
        image.append( [c for c in line] )
    fd.close()

    W, H = map(int, lines[0].split() )
    assert W == len(image[0])
    assert H == len(image)

    return W, H, image

def neighboors(x, y, W, H):
    res = []
    N = (
        (x+1, y), 
        #(x+1, y+1),
        (x, y+1),
        #(x-1, y+1),
        (x-1, y),
        #(x-1, y-1),
        (x, y-1),
        #(x+1, y-1),
        )

    for i, j in N:
        if i < 0 or i == W or j < 0 or j == H: continue
        if image[j][i] in ('W', 'R'):
            res.append( (i,j) )
    return res

L = []
def walk_rec(i, j):
    print i,j
    if visited[j][i]: return
    visited[j][i] = True

    # L = deepcopy(L)
    # L.append( (i,j) )
    L.append( (i,j) )

    if image[j][i] == 'R':
        print 'youpi'
        print L
        with open('maze-path.pickle', 'w') as f:
            f.write(pickle.dumps( L ))
        sys.exit(0)
    else:
        N = neighboors(i,j,W,H)
        for x, y in N:
            walk_rec(x, y)

    L.pop()

def walk(i, j):
    
    stack = []
    stack.append( (i,j) )

    while True:
        
        i, j = stack.pop()
        print j,i
        if image[j][i] == 'R':
            print 'youpi'
            return

        if False:
            if visited[j][i]: return
            visited[j][i] = True

        N = neighboors(i,j,W,H)
        for x, y in N:
            # if not visited[y][x]:
            stack.append( (x,y) )

if True:
    input = 'maze.txt'
    input = 'maze-mini.txt'
    input = sys.argv[1]
    W, H, image = deserialize(input)

    visited = [ [False for i in xrange(W)] for j in xrange(H) ]

    # maze_png = Image.open('maze.png')
    # W, H = maze_png.size

    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    # draw.setink( blue )

    # print 'Walking ...'
    # walk_rec(0, 2)
    # walk_rec(325, 194, [])
    # walk(2524, 410)
    # sys.exit(0)
    
# Maze
import Image, ImageDraw
photo = Image.new('RGB', (W, H), white)
draw = ImageDraw.Draw(photo)

colors = {
    'W': (255, 255, 255),
    'G': (0, 255, 0),
    'R': (255, 0, 0),
    'X': (128 , 0, 0),
    'Y': (0, 128, 0),
    'B': (0, 0, 0),
    '-': (0, 0, 0),
}

for j in xrange(H):
    for i in xrange(W):
        draw.point( (i,j), colors[image[j][i]] )


exec( open('maze_res.txt').read() )
for i,j in L:
    draw.point( (i,j), green )

photo.save('maze_res.png', "PNG")
sys.exit(0)

# Visited
photo = Image.new('RGB', (W, H), white)
draw = ImageDraw.Draw(photo)
for j in xrange(H):
    for i in xrange(W):
        if visited[j][i]:
            draw.point( (i,j), blue )

photo.save('maze_visited.png', "PNG")
