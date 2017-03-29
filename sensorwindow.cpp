#include "sensorwindow.h"

#include <QFrame>
#include <QHBoxLayout>
#include <QPushButton>
#include <QLabel>

sensorwindow::sensorwindow(QWidget *parent)
    :QFrame(parent)
{
    initSensorUI();
}

//------------------------------------------------

void sensorwindow::initSensorUI()
{
    QLabel * sensor_label = new QLabel;
    sensor_label->setText("Sensor Section");

    QPushButton * sensor_button = new QPushButton;
    sensor_button->setText("Sensor Button");

    QHBoxLayout * sensor_layout = new QHBoxLayout;
    sensor_layout->addWidget(sensor_label, 0, Qt::AlignCenter);
    sensor_layout->addWidget(sensor_button, 0, Qt::AlignRight);

    this->setLayout(sensor_layout);
    this->setStyleSheet("QFrame { background-color: yellow }");
}
