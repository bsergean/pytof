/***********************************************************************/
/* This example code demonstrates an OpenGL application program that   */
/*   displays a blue cube and a red pyramid in a simple X window.      */
/*                                                                     */
/*                                                                     */
/* The features of this example include:                               */
/*   - Opens an X window                                               */
/*   - Creates an OpenGL viewport                                      */
/*   - Renders a simple static world                                   */
/*                                                                     */
/* Considerations:                                                     */
/*   - A lot of code is necessary to open the GLX window (X w/ OpenGL) */
/*   - The main loop would typically watch for many more X Events      */
/*                                                                     */
/* This application uses the files:                                    */
/*   - shapes.c  (Bill Sherman's simple OpenGL shapes)                 */
/*                                                                     */
/* Copyright 1998, University of Illinois Board of Trustees            */
/***********************************************************************/
#include <stdio.h>

#include <GL/gl.h>
#include <GL/glx.h>

void	draw_world();

static int      snglBuf[] = {GLX_RGBA, GLX_DEPTH_SIZE, 16, None};
static int      dblBuf[] = {GLX_RGBA, GLX_DEPTH_SIZE, 16, GLX_DOUBLEBUFFER, None};

Display        *dpy;
Window          win;
GLboolean       doubleBuffer = GL_TRUE;


main(int argc, char* argv[])
{
	XVisualInfo    *vi;
	Colormap        cmap;
	XSetWindowAttributes swa;
	GLXContext      cx;
	XEvent          event;
	int             dummy;

	/********************************/
	/*** Initialize GLX routines  ***/
	/********************************/
	/*** open a connection to the X server ***/
	dpy = XOpenDisplay(NULL);
	if (dpy == NULL) {
		perror("could not open display");
		exit(0);
	}

	/*** make sure OpenGL's GLX extension supported ***/
	if (!glXQueryExtension(dpy, &dummy, &dummy)) {
		perror("X server has no OpenGL GLX extension");
		exit(0);
	}

	/*** find an appropriate visual ***/
	/* find an OpenGL-capable RGB visual with depth buffer */
	vi = glXChooseVisual(dpy, DefaultScreen(dpy), dblBuf);
	if (vi == NULL) {
		vi = glXChooseVisual(dpy, DefaultScreen(dpy), snglBuf);
		if (vi == NULL) {
			perror("no RGB visual with depth buffer");
			exit(0);
		}
		doubleBuffer = GL_FALSE;
	}
	if (vi->class != TrueColor) {
		perror("TrueColor visual required for this program");
		exit(0);
	}

	/*** create an OpenGL rendering context  ***/
	/* create an OpenGL rendering context */
	cx = glXCreateContext(dpy, vi, /* no sharing of display lists */ None,
			       /* direct rendering if possible */ GL_TRUE);
	if (cx == NULL) {
		perror("could not create rendering context");
		exit(0);
	}

	/*** create an X window with the selected visual ***/
	/* create an X colormap since probably not using default visual */
	cmap = XCreateColormap(dpy, RootWindow(dpy, vi->screen), vi->visual, AllocNone);
	swa.colormap = cmap;
	swa.border_pixel = 0;
	swa.event_mask = ExposureMask | ButtonPressMask | StructureNotifyMask;
	win = XCreateWindow(dpy, RootWindow(dpy, vi->screen), 0, 0, 300, 300, 0, vi->depth,
			    InputOutput, vi->visual, CWBorderPixel | CWColormap | CWEventMask, &swa);
	XSetStandardProperties(dpy, win, "glxsimple", "glxsimple", None, argv, argc, NULL);

	/*** bind the rendering context to the window ***/
	glXMakeCurrent(dpy, win, cx);

	/*** request the X window to be displayed on the screen ***/
	XMapWindow(dpy, win);

	/*** configure the OpenGL context for rendering ***/
	glEnable(GL_DEPTH_TEST);/* enable depth buffering */
	glDepthFunc(GL_LESS);	/* pedantic, GL_LESS is the default */
	glClearDepth(1.0);	/* pedantic, 1.0 is the default */
	/* frame buffer clears should be to black */
	glClearColor(0.0, 0.0, 0.0, 0.0);
	/* set up projection transform */
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 10.0);
	/* establish initial viewport */
	glViewport(0, 0, 300, 300);	/* pedantic, full window size is default viewport */


	/***************************/
	/*** do world simulation ***/
	/***************************/
	while (1) {
		do {
			XNextEvent(dpy, &event);
			switch (event.type) {
			case ConfigureNotify:
				glViewport(0, 0, event.xconfigure.width, event.xconfigure.height);
			}
		} while (XPending(dpy));

		/*** Handle projection ***/
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
		glTranslatef(0.0, -2.0, -3.0);

		/*** Render the world ***/
		draw_world();

		/*** Swap buffers (or flush GL cue) ***/
		if (doubleBuffer)
			glXSwapBuffers(dpy, win);
		else	glFlush();
	}
}



/* ----------------8<-----------------8<-----------------8<----------------*/
/* In a non-example applicatation, the following would be a separate file. */

		/**************************/
		/**************************/
		/** The Graphics section **/
		/**************************/
		/**************************/

void draw_cube();
void draw_pyramid();


/*********************/
/* draw_world(): ... */
/*********************/
void draw_world(void)
{
	glShadeModel(GL_SMOOTH);

	/**************************************/
	/* clear the screen -- very important */
	glClearColor(0.0, 0.0, 0.0, 0.0);
	glClearDepth(1.0);
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);

	/************************/
	/* draw all the objects */

	/* a blue cube */
	glColor3ub(100, 100, 255);
	glTranslatef(-2.0, 1.0, -6.0);
	draw_cube();

	/* a red pyramid */
	glColor3ub(255, 100, 100);
	glTranslatef(4.0, 0.0, 0.0);
	draw_pyramid();
}
