
#include "Texture.h"
#include <iostream>

#include <OpenEXR/ImfRgba.h>
#include <OpenEXR/ImfArray.h>
#include <OpenEXR/ImfRgbaFile.h>

Texture::Texture()
{
    mImage = NULL;
    mDepth = 4;
}

void
Texture::setSize(int width, int height)
{
    mW = width;
    mH = height;

    delete [] mImage;
    mImage = new unsigned char[mDepth * mW * mH];
}

//
// Found this here:
// http://oss.sgi.com/projects/ogl-sample/registry/EXT/texture_sRGB.txt
//
unsigned char
toChar(double val)
{
    double cl = val;

    double cs;
    if (isnan(cl)) {
        /* Map IEEE-754 Not-a-number to zero. */
        cs = 0.0;
    } else if (cl > 1.0) {
        cs = 1.0;
    } else if (cl < 0.0) {
        cs = 0.0;
    } else if (cl < 0.0031308) {
        cs = 12.92 * cl;
    } else {
        cs = 1.055 * pow(cl, 0.41666) - 0.055;
    }
    double csi = floor(255.0 * cs + 0.5);
    return (unsigned char) csi;
}

bool
Texture::read(const char fn [])
{
    Imf::RgbaInputFile file(fn); 
    Imath::Box2i dw = file.dataWindow();
    int width  = dw.max.x - dw.min.x + 1; 
    int height = dw.max.y - dw.min.y + 1; 

    Imf::Array2D<Imf::Rgba> pixels;
    pixels.resizeErase(height, width);

    file.setFrameBuffer(
        &pixels[0][0] - dw.min.x - dw.min.y * width, 
        1, width);

    file.readPixels(dw.min.y, dw.max.y);

    setSize(width, height);

    for (int j = 0; j < height; ++j) {
        for (int i = 0; i < width; ++i) {

            unsigned char R, G, B, A;
            R = toChar(pixels[i][j].r);
            G = toChar(pixels[i][j].g);
            B = toChar(pixels[i][j].b);
            A = toChar(pixels[i][j].a);

            mImage[mDepth * (j * width + i)]   = B;
            mImage[mDepth * (j * width + i)+1] = G;
            mImage[mDepth * (j * width + i)+2] = R;
            mImage[mDepth * (j * width + i)+3] = A;
        }
    }

    return true;
}

int
Texture::init()
{
    glGenTextures(1, &mTexname);
    glBindTexture(GL_TEXTURE_2D, mTexname);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, 
                    GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, 
                    GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, 
                    GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, 
                    GL_LINEAR);

    int width  = mW;
    int height = mH;
    int border = 0;
    int level  = 0;

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glPixelStorei(GL_PACK_ALIGNMENT, 1);

    glTexImage2D(GL_TEXTURE_2D, level, GL_RGBA, 
                 width, height, border, 
                 GL_BGRA_EXT, GL_UNSIGNED_BYTE, 
                 mImage);

    return mTexname;
}
