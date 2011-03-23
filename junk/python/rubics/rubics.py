#! /usr/bin/env python
''' Initial glut display code From cube.py, 
Converted to Python by Jason Petrone 6/00
(there was no depth bit, took some time to figure it out ...)
'''

import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print '''
  ERROR: PyOpenGL not installed properly.
          '''

# http://en.wikipedia.org/wiki/Web_colors
black = [0, 0, 0]
white = [0xFF, 0xFF, 0xFF]

red =   [0xFF, 0, 0]
green = [0x22, 0x8B, 0]
blue =  [0x46, 0x82, 0xB4]

yellow = [0xFF, 0xD7, 0]
orange = [0xFF, 0x45, 0]

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
    print Front
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

def draw_rubics():
    # One
    glPushMatrix()
    glTranslatef(0.0, 0.0, -1.0)
    draw_face()
    glPopMatrix()

    # two
    glPushMatrix()
    draw_face()
    glPopMatrix()

    # three
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    draw_face()
    glPopMatrix()

def draw_face():

    # One
    glPushMatrix()

    glTranslatef(-1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glTranslatef(1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glTranslatef(1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glPopMatrix()

    # Two
    glPushMatrix()

    glTranslatef(0.0, 1.0, 0.0)
    glTranslatef(-1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glTranslatef(1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glTranslatef(1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glPopMatrix()

    # Three
    glPushMatrix()

    glTranslatef(0.0, -1.0, 0.0)
    glTranslatef(-1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glTranslatef(1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glTranslatef(1.0, 0.0, 0.0)
    # glutWireCube (1.0)
    draw_cube()

    glPopMatrix()

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
    gluLookAt (+4.0, +4.0, +5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glScalef (1.3, 1.3, 1.3)      # modeling transformation
    draw_rubics()

    glFlush ()

def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode (GL_MODELVIEW)

def keyboard(key, x, y):
    if key == chr(27):
        import sys
        sys.exit(0)

glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize (500, 500)
glutInitWindowPosition (100, 100)
glutCreateWindow ('cube')
init ()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMainLoop()

class Rubics:
    def __init__(self): pass
