#pragma once

#include <OpenGL/gl.h>

class Texture
{
public:
    Texture();

    bool read(const char fn []);
    int init();
    void setSize(int width, int height);

    int width()  const { return mW; }
    int height() const { return mH; }

    GLuint mTexname;

private:
    unsigned mW, mH, mDepth;
    unsigned char* mImage;
};
