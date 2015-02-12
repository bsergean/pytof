#include "SoloLightsDialog.h"
#include <QApplication>

int 
main(int argv, char **args)
{
    QApplication app(argv, args);

    std::vector<std::string> lights;
    lights.push_back("spot");
    lights.push_back("env");
    lights.push_back("direct");
    SoloLightsDialog d(lights);
    d.show();

    puts("caca");

    return app.exec();
}
