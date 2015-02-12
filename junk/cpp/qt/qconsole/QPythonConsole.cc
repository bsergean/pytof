#include "SoloLightsDialog.h"

#include <QtGui/QListWidget>
#include <QtGui/QMessageBox>
#include <QtCore/QDebug>

SoloLightsDialog::SoloLightsDialog(std::vector<std::string> lights)
{
    mListWidget = new QListWidget(this);

    mListWidget->setSelectionMode(
        QAbstractItemView::MultiSelection);

    for (unsigned i = 0; i < lights.size(); ++i) {
        QString itemName = QString::fromStdString(lights[i]);
        QListWidgetItem* item = new QListWidgetItem(
            itemName, mListWidget);
        item->setFlags(item->flags() | 
                       Qt::ItemIsUserCheckable);
        item->setToolTip("light -> " + itemName);
        item->setData(Qt::UserRole, QVariant("caca " + itemName));
        // item->setCheckState(Qt::Unchecked);
        item->setCheckState(Qt::Checked);
    }

    connect(mListWidget, SIGNAL(itemChanged(QListWidgetItem*)), 
            this, SLOT(userCheckedOrUncheckedAnItem(QListWidgetItem*)));
}

void
SoloLightsDialog::userCheckedOrUncheckedAnItem(
    QListWidgetItem *item)
{
  if (item->checkState() == Qt::Checked) {
    qDebug() << "checked " << item->text() << " " << item->data(Qt::UserRole).toString();
  } else {
    qDebug() << "unchecked " << item->text() << " " << item->data(Qt::UserRole);
  }
}
