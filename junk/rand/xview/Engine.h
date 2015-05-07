#include "Texture.h"
#include <string>

namespace xview {

class Engine
{
public:
    Engine() : mInitialized(false) {}

    void init(const std::string& filename);

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
