#ifndef CUSTOMTABLEWIDGET_H
#define CUSTOMTABLEWIDGET_H

#include <QTableWidget>

QT_BEGIN_NAMESPACE
class QTableWidgetItem;
QT_END_NAMESPACE

class customTableWidget : public QTableWidget
{
     Q_OBJECT
public:
     customTableWidget( QWidget *parent = 0 );
     ~customTableWidget();
private slots:
     void selectRow( const QModelIndex& );
protected:
     void editItem( QTableWidgetItem * item) ;
};

#endif // CUSTOMTABLEWIDGET_H
