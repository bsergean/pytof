#include "Texture.h"

namespace xview {

class Engine
{
public:
    Engine() : mInitialized(false) {}

    void init();

    void render();
    void reshape(int w, int h);

    int width() const  { return mWidth; }
    int height() const { return mHeight; }

private:
    int mWidth;
    int mHeight;
    Texture mTexture;
    bool mInitialized;
};

}
