
#include <stdio.h>
#include <stdlib.h>
#include <GLUT/glut.h>
#include "engine.h"

static xview::Engine engine;

void 
xview_mouse(int button, int button_state, 
            int x, int y) 
{
    /*engine.button = button;
    engine.motion = button_state;
    OglSdk::mouse m = { x, y };
    engine.mouse_start = m;
    */

    glutPostRedisplay(); // ask for a refresh
}

void 
xview_display(void) 
{
    engine.render();
    glutSwapBuffers(); 
}

void 
xview_reshape(int w, int h) 
{
    engine.reshape(w, h);
    glutSwapBuffers();
}

void 
xview_processNormalKeys(unsigned char key, 
                        int x, int y) 
{
    printf("xview_processNormalKeys %d\n", key);
    if (key == 27) exit(0);
}

void 
xview_processSpecialKeys(int key, int x, int y) 
{
	if      (key == GLUT_KEY_LEFT)  { puts("left"); }
	else if (key == GLUT_KEY_RIGHT) { puts("left"); }
	else if (key == GLUT_KEY_DOWN)  { puts("left"); }
	else if (key == GLUT_KEY_UP)    { puts("left"); }
}

int 
main(int argc, char** argv) 
{
    if (argc != 2) {
        puts("Usage: xview <filename>");
        return -1;
    }

    std::string filename(argv[1]);

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGBA  | GLUT_DOUBLE |
                        GLUT_DEPTH | GLUT_MULTISAMPLE);

    engine.init(filename);
    glutInitWindowSize(engine.width(), engine.height());
    (void) glutCreateWindow("xview");
    // glutFullScreen();

    // Events
    glutKeyboardFunc(xview_processNormalKeys);
    glutSpecialFunc(xview_processSpecialKeys);
    glutMouseFunc(xview_mouse);

    glutDisplayFunc(xview_display);
    glutReshapeFunc(xview_reshape);

    glutMainLoop();
}

