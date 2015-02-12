#pragma once

#include <QtGui/QDialog>

class QListWidget;
class QListWidgetItem;

class SoloLightsDialog: public QDialog
{
    Q_OBJECT

public:
    SoloLightsDialog(std::vector<std::string> lights);
    ~SoloLightsDialog() {}

public slots:
    void userCheckedOrUncheckedAnItem(
        QListWidgetItem *item);

private:
    QListWidget *mListWidget;
};
