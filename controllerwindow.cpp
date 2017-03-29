#include "controllerwindow.h"

#include <QFrame>
#include <QHBoxLayout>
#include <QPushButton>
#include <QLabel>

controllerwindow::controllerwindow(QWidget *parent)
    :QFrame(parent)
{
    initControllerUI();
}

//------------------------------------------------

void controllerwindow::initControllerUI()
{
    QLabel * controller_label = new QLabel;
    controller_label->setText("Controller Section");

    QPushButton * controller_button = new QPushButton;
    controller_button->setText("Controller Button");

    QHBoxLayout * controller_layout = new QHBoxLayout;
    controller_layout->addWidget(controller_label, 0, Qt::AlignCenter);
    controller_layout->addWidget(controller_button, 0, Qt::AlignCenter);

    this->setLayout(controller_layout);
    this->setStyleSheet("QFrame { background-color: red }");
}
