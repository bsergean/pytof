#pragma once

#include <QtGui/QDialog>
#include <QtGui/QPainter>

class QListWidget;
class QListWidgetItem;

typedef std::pair<std::string, size_t> DirInfo;
typedef std::vector<DirInfo> DirInfoList;

class RadialDiskView: public QDialog
{
    Q_OBJECT

public:
    RadialDiskView(const DirInfoList& dirInfoList);
    ~RadialDiskView() {}

protected:
    void paintEvent(QPaintEvent *event);

private:
    DirInfoList mDirInfoList;
};
