#include "RadialDiskView.h"

#include <QtGui/QListWidget>
#include <QtGui/QMessageBox>
#include <QtCore/QDebug>

RadialDiskView::RadialDiskView(const DirInfoList& dirInfoList)
{
    mDirInfoList = dirInfoList;
}

QPainterPath
drawRegion(
    int x, 
    int y,
    double startAngle,
    double sweepLength)
{
    QPainterPath path;

    QRectF rectangle;
    rectangle = QRectF(x, y, 500, 500);

    path.arcMoveTo(rectangle, 45);
    path.arcTo(rectangle, 45, 30);

    QPointF current = path.currentPosition();

    QPainterPath pathB;
    rectangle = QRectF(250 - 25, 250 - 25, 50, 50);

    pathB.arcMoveTo(rectangle, 45 + 30);
    pathB.arcTo(rectangle, 45 + 30, -30);

    path.connectPath(pathB);
    path.closeSubpath();

    return path;
}

void
RadialDiskView::paintEvent(QPaintEvent * /*event*/)
{
    //create a QPainter and pass a pointer to the device.
    //A paint device can be a QWidget, a QPixmap or a QImage
    QPainter painter(this);

#if 1
    QPainterPath path = drawRegion(0, 0, 0, 0);
    QLinearGradient myGradient;
    painter.setBrush(myGradient);
    painter.drawPath(path);
    return;
#endif

    QRectF rectangle;
    int startAngle, spanAngle; 

    rectangle = QRectF(0, 0, 200, 200);
    startAngle = 45 * 16;
    spanAngle  = 90 * 16;

    painter.drawArc(rectangle, startAngle, spanAngle);
    painter.drawRect(rectangle);
    painter.drawText(100, 100, "3.6G");

    rectangle = QRectF(50, 50, 100, 100);
    startAngle = 45 * 16;
    spanAngle  = 90 * 16;

    painter.drawArc(rectangle, startAngle, spanAngle);
    painter.drawRect(rectangle);
 
    //a simple line

    painter.drawLine(width() / 2, 
                     height() / 2,
                     0, 0);

    painter.drawLine(width() / 2, 
                     height() / 2,
                     width(), height());
 
//     //create a black pen that has solid line
//     //and the width is 2.
//     QPen myPen(Qt::black, 2, Qt::SolidLine);
//     painter.setPen(myPen);
//     painter.drawLine(100,100,100,1);
//  
//     //draw a point
//     myPen.setColor(Qt::red);
//     painter.drawPoint(110,110);
//  
//     //draw a polygon
//     QPolygon polygon;
//     polygon << QPoint(130, 140) << QPoint(180, 170)
//              << QPoint(180, 140) << QPoint(220, 110)
//              << QPoint(140, 100);
//      painter.drawPolygon(polygon);
//  
//      //draw an ellipse
//      //The setRenderHint() call enables antialiasing, telling QPainter to use different
//      //color intensities on the edges to reduce the visual distortion that normally
//      //occurs when the edges of a shape are converted into pixels
//      painter.setRenderHint(QPainter::Antialiasing, true);
//      painter.setPen(QPen(Qt::black, 3, Qt::DashDotLine, Qt::RoundCap));
//      painter.setBrush(QBrush(Qt::green, Qt::SolidPattern));
//      painter.drawEllipse(200, 80, 400, 240);
}
