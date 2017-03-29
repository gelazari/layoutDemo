#ifndef SENSORWINDOW_H
#define SENSORWINDOW_H

#include <QWidget>
#include <QFrame>

class sensorwindow: public QFrame
{
    Q_OBJECT
public:
    sensorwindow(QWidget * parent);

private:
    void initSensorUI();
};

#endif // SENSORWINDOW_H
