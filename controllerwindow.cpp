#include "controllerwindow.h"

#include <QFrame>
#include <QVBoxLayout>
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

    QPushButton * controller_button1 = new QPushButton;
    controller_button1->setText("Controller Button_1");
    QPushButton * controller_button2 = new QPushButton;
    controller_button2->setText("Controller Button_2");
    QPushButton * controller_button3 = new QPushButton;
    controller_button3->setText("Controller Button_3");
    QPushButton * controller_button4 = new QPushButton;
    controller_button4->setText("Controller Button_4");

    QVBoxLayout * controller_layout = new QVBoxLayout;
    controller_layout->addWidget(controller_label, 0, Qt::AlignCenter);
    controller_layout->addWidget(controller_button1, 0, Qt::AlignCenter);
    controller_layout->addWidget(controller_button2, 0, Qt::AlignCenter);
    controller_layout->addWidget(controller_button3, 0, Qt::AlignCenter);
    controller_layout->addWidget(controller_button4, 0, Qt::AlignCenter);
    //this->setFixedWidth(150);
    QFrame * controller_frame = new QFrame;
    controller_frame->setStyleSheet("QFrame { background-color: green }");
    controller_frame->setFixedWidth(200);
    controller_frame->setLayout(controller_layout);

    QHBoxLayout * section_layout = new QHBoxLayout;
    section_layout->addWidget(controller_frame);
    QFrame * controller_section = new QFrame;
    controller_section->setFixedWidth(150);
    controller_section->setLayout(section_layout);

    this->setLayout(section_layout);
    this->setStyleSheet("QFrame { background-color: grey }");
}
