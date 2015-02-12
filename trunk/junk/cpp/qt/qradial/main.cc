#include "RadialDiskView.h"
#include <QApplication>

int 
main(int argv, char **args)
{
    QApplication app(argv, args);

    DirInfoList dirInfoList;
    dirInfoList.push_back(DirInfo("Documents", 20));
    dirInfoList.push_back(DirInfo("Music", 50));
    dirInfoList.push_back(DirInfo("Pictures", 30));
    RadialDiskView diskView(dirInfoList);
    diskView.show();

    puts("caca");

    return app.exec();
}
