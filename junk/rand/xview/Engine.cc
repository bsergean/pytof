#include "Engine.h"

#include "Texture.h"
#include <iostream>
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>

namespace xview {

void
Engine::init(const std::string& filename)
{
    mTexture.read(filename.c_str());

    mWidth  = mTexture.width();
    mHeight = mTexture.height();
}

void
Engine::render()
{
    if (!mInitialized) {
        mTexture.init();
        mInitialized = true;
    }

    int w = mWidth;
    int h = mHeight;

    glEnable(GL_LIGHT0);
    glEnable(GL_LIGHTING);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_COLOR_MATERIAL);
    glColorMaterial(GL_FRONT, GL_DIFFUSE);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluOrtho2D(0, w, 0, h);

    glMatrixMode(GL_MODELVIEW);

    glLoadIdentity();

#if 0
    // Default OpenGL camera
    gluLookAt(0.0, 0.0, 0.0,  // eye
              0.0, 0.0, -1.0, // target
              0.0, 1.0, 0.0); // Y+ is up
#endif

    // (222, 222, 222, 255)
    float grey = 222. / 255;
    glClearColor(grey, grey, grey, 1.0f);
    // glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, mTexture.mTexname);
    // Textured background
    glBegin(GL_QUADS);
    float depth = 0.5;
    glTexCoord2d(0.0,0.0); glVertex3f(0.0, 0.0, depth);
    glTexCoord2d(1.0,0.0); glVertex3f(w  , 0.0, depth);
    glTexCoord2d(1.0,1.0); glVertex3f(w  , h  , depth);
    glTexCoord2d(0.0,1.0); glVertex3f(0  , h  , depth);
    glEnd();
    glDisable(GL_TEXTURE_2D);

    glMatrixMode(GL_PROJECTION);
    glMatrixMode(GL_MODELVIEW);
}

void
Engine::reshape(int width, int height)
{
    printf("reshape / not implemented: %d %d\n", width, height);
    // see https://www3.ntu.edu.sg/home/ehchua/programming/opengl/CG_Introduction.html
}

} // namespace
