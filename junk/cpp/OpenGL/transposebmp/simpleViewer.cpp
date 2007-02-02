#include "simpleViewer.h"
#include <math.h>

using namespace std;

// Draws a spiral
void Viewer::draw()
{
  glBegin(GL_POLYGON);
    glColor3f(1.0f, 0.0f, 0.1f);
    glVertex2f(0.0, 0.0);
    glVertex2f(0.0, 1.0);
    glVertex2f(1.0, 1.0);
  glEnd();
}

void Viewer::init()
{
  // Restore previous viewer state.
  restoreFromFile();

  help();
}

QString Viewer::helpString() const
{
  QString text("<h2>S i m p l e V i e w e r</h2>");
  text += "Use the mouse to move the camera around the object. ";
  text += "You can revolve around, zoom and translate with the three buttons. ";
  text += "Left and middle buttons pressed together rotate around the camera z axis<br><br>";
  text += "Pressing <b>Alt</b> and one of the function key (<b>F1</b>..<b>F12</b>) defines a camera keyFrame. ";
  text += "Simply press the function key again to restore it. Several keyFrames define a ";
  text += "camera path. Paths are saved when you quit the application.<br><br>";
  text += "Press <b>F</b> to display the frame rate, <b>A</b> for the world axis, ";
  text += "<b>Alt+Return</b> for full screen mode and <b>Control+S</b> to save a snapshot.<br><br>";
  text += "A left button double click aligns the closer axis with the camera (if close enough). A middle button ";
  text += "double click fits the zoom of the camera and the right button re-centers the scene.<br>";
  text += "A left button double click while holding right button pressed defines the <i>Revolve Around Point</i>.";
  text += "With middle button holded instead, it zooms on the pixel.<br><br>";
  text += "See also the <b>Keyboard</b> and <b>Mouse</b> tabs and the documentation web pages.<br>";
  text += "Press <b>Escape</b> to exit the viewer.";
  return text;
}
