#pragma once

#include <QtGui/QDialog>

class QListWidget;
class QListWidgetItem;

class QPythonConsole: public QDialog
{
    Q_OBJECT

public:
    QPythonConsole();
    ~QPythonConsole() {}

public slots:
    void userCheckedOrUncheckedAnItem(
        QListWidgetItem *item);

private:
    QListWidget *mListWidget;
};
