#! /usr/bin/env python
# coding: utf-8
''' Initial glut display code From cube.py, 
Converted to Python by Jason Petrone 6/00
(there was no depth bit, took some time to figure it out ...)

http://rubikscube.info/beginner-corners.php

Unicode arrows
http://en.wikipedia.org/wiki/Arrow_(symbol)
'''

import sys, os

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print '''
  ERROR: PyOpenGL not installed properly.
          '''

from colors import *
from cube_ops import *
from rotate_ops import *

import pickle
fn = 'floppy.pickle'

# ↷ 
# def R():
#     return None    

# Back to front: f1, f2, f3
def reset():
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
    f3 = [
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

    return f1, f2, f3

X, Y, Z = +4.0, +4.0, +5.0

def draw_cube_helper(Front   = None,
                     Back    = None,
                     Top     = None,
                     Bottom  = None,
                     Right   = None,
                     Left    = None):

    if Front  is None: Front   = green
    if Back   is None: Back    = red
    if Top    is None: Top     = white
    if Bottom is None: Bottom  = yellow
    if Right  is None: Right   = red
    if Left   is None: Left    = orange

    size = 0.5
    xmin, ymin, zmin = [-size, -size, -size]
    xmax, ymax, zmax = [+size, +size, +size]

    glBegin(GL_QUADS)

    # Front Face
    glColor3ub(*Front)
    glVertex3f( xmin,  ymin,  zmax)	# Bottom Left Of The Texture and Quad
    glVertex3f( xmax,  ymin,  zmax)	# Bottom Right Of The Texture and Quad
    glVertex3f( xmax,  ymax,  zmax)	# Top Right Of The Texture and Quad
    glVertex3f( xmin,  ymax,  zmax)	# Top Left Of The Texture and Quad

    # Back Face
    glColor3ub(*Back)
    glVertex3f( xmin,  ymin,  zmin)	# Bottom Right Of The Texture and Quad
    glVertex3f( xmin,  ymax,  zmin)	# Top Right Of The Texture and Quad
    glVertex3f( xmax,  ymax,  zmin)	# Top Left Of The Texture and Quad
    glVertex3f( xmax,  ymin,  zmin)	# Bottom Left Of The Texture and Quad

    # Top Face
    glColor3ub(*Top)
    glVertex3f( xmin,  ymax,  zmin)	# Top Left Of The Texture and Quad
    glVertex3f( xmin,  ymax,  zmax)	# Bottom Left Of The Texture and Quad
    glVertex3f( xmax,  ymax,  zmax)	# Bottom Right Of The Texture and Quad
    glVertex3f( xmax,  ymax,  zmin)	# Top Right Of The Texture and Quad

    # Bottom Face       
    glColor3ub(*Bottom)
    glVertex3f( xmin,  ymin,  zmin)	# Top Right Of The Texture and Quad
    glVertex3f( xmax,  ymin,  zmin)	# Top Left Of The Texture and Quad
    glVertex3f( xmax,  ymin,  zmax)	# Bottom Left Of The Texture and Quad
    glVertex3f( xmin,  ymin,  zmax)	# Bottom Right Of The Texture and Quad

    # Right face
    glColor3ub(*Right)
    glVertex3f( xmax,  ymin,  zmin)	# Bottom Right Of The Texture and Quad
    glVertex3f( xmax,  ymax,  zmin)	# Top Right Of The Texture and Quad
    glVertex3f( xmax,  ymax,  zmax)	# Top Left Of The Texture and Quad
    glVertex3f( xmax,  ymin,  zmax)	# Bottom Left Of The Texture and Quad

    # Left Face
    glColor3ub(*Left)
    glVertex3f( xmin,  ymin,  zmin)	# Bottom Left Of The Texture and Quad
    glVertex3f( xmin,  ymin,  zmax)	# Bottom Right Of The Texture and Quad
    glVertex3f( xmin,  ymax,  zmax)	# Top Right Of The Texture and Quad
    glVertex3f( xmin,  ymax,  zmin)	# Top Left Of The Texture and Quad

    glEnd()

class Wireframe(object):
    def __init__(self, width = None, color = None):
        self.line_width = 3.0
        if width is not None:
            self.line_width = width

        self.color = [1.0, 1.0, 1.0]
        if color is not None:
            self.color = color

    def __enter__(self):
        # color = [0.10, 0.10, 0.10]
        # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, color)
        # glColor3f(*color)

        glPushAttrib( GL_ALL_ATTRIB_BITS )

        # Enable polygon offsets, and offset filled polygons 
        # forward by 2.5
        glEnable( GL_POLYGON_OFFSET_FILL )
        glPolygonOffset( -2.5, -2.5 )

        # Set the render mode to be line rendering with a 
        # thick line width
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glLineWidth( self.line_width )

        # Set the colour to be white
        glColor3f( *self.color )

    def __exit__(self, ty, val, tb):
        # Pop the state changes off the attribute stack
        # to set things back how they were
        glPopAttrib()
        return False

def draw_wire_cube():
    with Wireframe(5.0):
        draw_cube_helper(black, black, black, 
                         black, black, black)

def draw_solid_cube(a=None, b=None, c=None, d=None, e=None, f=None):
    draw_cube_helper(a, b, c, d, e, f)

def draw_cube(a=None, b=None, c=None, d=None, e=None, f=None):
    draw_solid_cube(a, b, c, d, e, f)
    draw_wire_cube()

def init():
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def draw_rubics(f1, f2, f3):
    # One
    glPushMatrix()
    glTranslatef(0.0, 0.0, -1.0)
    draw_face(f1)
    glPopMatrix()

    # two
    glPushMatrix()
    draw_face(f2)
    glPopMatrix()

    # three
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    draw_face(f3)
    glPopMatrix()

def draw_face(facets):
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = facets

    # One
    glPushMatrix()
    glTranslatef(-1.0, 0.0, 0.0)
    draw_cube(*c4)
    glTranslatef(1.0, 0.0, 0.0)
    draw_cube(*c5)
    glTranslatef(1.0, 0.0, 0.0)
    draw_cube(*c6)
    glPopMatrix()

    # Two
    glPushMatrix()
    glTranslatef(0.0, 1.0, 0.0)
    glTranslatef(-1.0, 0.0, 0.0)
    draw_cube(*c1)
    glTranslatef(1.0, 0.0, 0.0)
    draw_cube(*c2)
    glTranslatef(1.0, 0.0, 0.0)
    draw_cube(*c3)
    glPopMatrix()

    # Three
    glPushMatrix()
    glTranslatef(0.0, -1.0, 0.0)
    glTranslatef(-1.0, 0.0, 0.0)
    draw_cube(*c7)
    glTranslatef(1.0, 0.0, 0.0)
    draw_cube(*c8)
    glTranslatef(1.0, 0.0, 0.0)
    draw_cube(*c9)
    glPopMatrix()

def draw():
    # Back to front: f1, f2, f3
    draw_rubics(f1, f2, f3)

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glEnable (GL_DEPTH_TEST)
    glEnable (GL_LINE_SMOOTH)

    # glPolygonMode(GL_BACK,GL_FILL)
    # glPolygonMode(GL_FRONT,GL_FILL)

    glColor3f (1.0, 1.0, 1.0)
    glLoadIdentity ()             # clear the matrix
    # viewing transformation
    print X, Y, Z
    gluLookAt (X, Y, Z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glScalef (1.3, 1.3, 1.3)      # modeling transformation
    draw()

    glFlush ()

def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    # glOrtho (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode (GL_MODELVIEW)

def keyboard(key, x, y):
    global f1, f2, f3
    global X, Y, Z

    if key == chr(27):

        pickle.dump( (f1, f2, f3, stack), open( fn, "wb" ) ) 

        import sys
        sys.exit(0)

    # Views
    elif key == '1':
        X, Y, Z = +4.0, +4.0, +5.0
    elif key == '2':
        X, Y, Z = -4.5, +4.0, +5.0
    elif key == '3':
        X, Y, Z = +4.0, +4.0, -5.0
    elif key == '4':
        X, Y, Z = -4.0, +4.0, -5.0

    # 0 = useless ?
    elif key == '0':
        f1, f2, f3 = rubicUpsideDown(f1, f2, f3)

    # vi forever ;)
    elif key == 'l':
        f1, f2, f3 = rubicRight(f1, f2, f3)
    elif key == 'h':
        f1, f2, f3 = rubicLeft(f1, f2, f3)
    elif key == 'k':
        f1, f2, f3 = rubicUp(f1, f2, f3)
    elif key == 'j':
        f1, f2, f3 = rubicDown(f1, f2, f3)
        display()

    # Moves
    # Frontal rotation
    elif key == 'y':
        f1, f2, f3 = rubicC(f1, f2, f3)
    elif key == 'r':
        f1, f2, f3 = rubicCC(f1, f2, f3)
    elif key == 'h':
        f1, f2, f3 = rubicF2C(f1, f2, f3)
    elif key == 'n':
        f1, f2, f3 = rubicF1C(f1, f2, f3)

    # Slice rotation
    elif key == 'e':
        f1, f2, f3 = rubicTR(f1, f2, f3)
    elif key == 'q':
        f1, f2, f3 = rubicTL(f1, f2, f3)
    elif key == 'd':
        f1, f2, f3 = rubicMR(f1, f2, f3)
    elif key == 'a':
        f1, f2, f3 = rubicML(f1, f2, f3)
    elif key == 'c':
        f1, f2, f3 = rubicBR(f1, f2, f3)
    elif key == 'z':
        f1, f2, f3 = rubicBL(f1, f2, f3)

    # Up and down
    elif key == 'o':
        f1, f2, f3 = rubicRU(f1, f2, f3)
    elif key == '.':
        f1, f2, f3 = rubicRD(f1, f2, f3)
    elif key == 'i':
        f1, f2, f3 = rubicMU(f1, f2, f3)
    elif key == ',':
        f1, f2, f3 = rubicMD(f1, f2, f3)
    elif key == 'u':
        f1, f2, f3 = rubicLU(f1, f2, f3)
    elif key == 'm':
        f1, f2, f3 = rubicLD(f1, f2, f3)

    # twist randomly
    elif key == '`':
        f1, f2, f3 = randomize(f1, f2, f3)
    # reset
    elif key == '~':
        f1, f2, f3 = reset()

    if key == '-':
        if stack:
            f1, f2, f3 = stack.pop()
        else: # not sure we need that else
            f1, f2, f3 = reset() 
    else:
        stack.append( (f1, f2, f3) )

    display()

# globals
if os.path.exists(fn):
    f1, f2, f3, stack = pickle.load(open(fn))
else: 
    f1, f2, f3 = reset() 
    stack = []

glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize (500, 500)
glutInitWindowPosition (1200, 100)
glutCreateWindow ('Rubicul')
init ()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMainLoop()

class Rubics:
    def __init__(self): pass
