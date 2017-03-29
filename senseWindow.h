#ifndef SENSEWINDOW_H
#define SENSEWINDOW_H

#include <QWidget>
#include <QMainWindow>

QT_BEGIN_NAMESPACE
class QLabel;
class QFrame;
class QIcon;
class QTableWidgetItem;
class QPushButton;
class customStackedWidget;
QT_END_NAMESPACE

class senseWindow : public QMainWindow
{
    Q_OBJECT

public:
    senseWindow(QWidget * parent = 0);

    enum Section {Sensor, Controller, Analysis, StackUp, Pattern, Traces};

private:
    QLabel * createLabel(const QString & text);
    QFrame * createTopLayout();
    QFrame * createLeftLayout();
    QFrame * createCentralLayout();
    QTableWidgetItem * createTableWidgetItem( const QString & text );
    QTableWidgetItem * createHeaderItem( const QString & text);
    QIcon getIconFromPath( const QString & iconPath );
    QFrame * createSimluationSummaryFrame();
    QPushButton * createLeftPanelPushButton( const QString & text, const QIcon & icon);
    QWidget * createSection(const Section & section);
    customStackedWidget *central_widget;
    QWidget * the_central_widget;
};

#endif // SENSEWINDOW_H
