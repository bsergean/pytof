#include "QPythonConsole.h"
#include <QApplication>

int 
main(int argv, char **args)
{
    QApplication app(argv, args);

    QPythonConsole console;
    console.show();

    return app.exec();
}
