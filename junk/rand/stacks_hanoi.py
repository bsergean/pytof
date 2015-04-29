
from PIL import Image, ImageDraw

#
# ffmpeg -i out_%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
# I think this still didn't work when played under Safari with <video> so 
# I had to convert it with Handbrake.
#

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

class Canvas():
    def __init__(self, W, H):
        self.W = W
        self.H = H
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

    def draw_stack(self, delta, stack):
        color = blue

        N = len(stack)

        y = 20
        yBuf = 10

        for step, x in enumerate(stack):
            i = 0 + delta
            j = self.H - y - yBuf

            j -= step * y

            A = (i - x/2, j)
            B = (i + x/2, j)
            C = (i + x/2, j + y)
            D = (i - x/2, j + y)

            self.draw.line([A, B, C, D, A], color, 5)

    def save(self, output):
        self.photo.rotate(180)
        self.photo.save(output, "PNG")

import sys

N = 6

s1 = []
x = 180
for i in xrange(N):
    s1.append(x)
    x -= 15

print s1

s2 = []
s3 = []

class Op:
    def __init__(self, pop, push):
        self.pop = pop
        self.push = push

    def move(self):
        val = -1
        if self.pop == '1': 
            val = s1[-1]
            s1.pop()
        elif self.pop == '2':
            val = s2[-1]
            s2.pop()
        elif self.pop == '3':
            val = s3[-1]
            s3.pop()

        if self.push == '1': s1.append(val)
        elif self.push == '2': s2.append(val)
        elif self.push == '3': s3.append(val)

ops = []
for line in sys.stdin:
    pop, push = line.split()
    print pop, push

    op = Op(pop, push)
    ops.append(op)

digits = len(str(len(ops)))
step = 0

def drawStep(step, digits):
    canvas = Canvas(600, 256)
    canvas.draw_stack(100, s1)
    canvas.draw_stack(300, s2)
    canvas.draw_stack(500, s3)
    fn = 'out_%s.png' % (str(step).zfill(digits))
    canvas.save(fn)

drawStep(0, digits)
step += 1

for op in ops:
    op.move()

    drawStep(step, digits)
    step += 1
