#ifndef CONTROLLERWINDOW_H
#define CONTROLLERWINDOW_H

#include <QWidget>
#include <QFrame>

class controllerwindow: public QFrame
{
    Q_OBJECT
public:
    controllerwindow(QWidget * parent);

private:
    void initControllerUI();
};

#endif // CONTROLLERWINDOW_H
